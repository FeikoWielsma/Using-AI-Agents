"""Prepared Colab controls for the exploration activities."""
from pathlib import Path
import base64
import json
import exploration_runtime as runtime

def show(client,lessons):
    import ipywidgets as w
    from IPython.display import display, clear_output
    states={l['id']:runtime.initial() for l in lessons}
    choose=w.Dropdown(options=[(l['title'],l['id']) for l in lessons],description='Activity')
    task=w.Textarea(layout=w.Layout(width='100%',height='130px'))
    team=w.Checkbox(value=True,description='Two specialists + coordinator')
    specialist=w.Dropdown(options=['operations','accessibility'],description='Specialist')
    discount=w.Checkbox(description='Discount from EUR 50')
    run=w.Button(description='Run the agent',button_style='primary');reset=w.Button(description='Reset activity')
    approve=w.Button(description='Approve refund');reject=w.Button(description='Reject refund')
    boundary=w.Button(description='Try EUR 80 limit')
    download=w.Button(description='Download outputs');output=w.Output();intro=w.Output()
    def render():
        with output:
            clear_output();s=states[choose.value];print(s['answer'])
            for a in s['agents']:print('\n'+a['role']+'\n'+a['answer'])
            if s['pending']:print('\nAwaiting your decision:',json.dumps(s['pending']))
            if choose.value==4:print('\nFictional ledger:',json.dumps(s['ledger']))
            if choose.value==5:print('\nCurrent code:\ndef total(price, quantity):\n    return '+s['expression'])
            if s.get('seconds') is not None:print('\nSeconds:',s['seconds'],'Reported tokens:',s['tokens'])
            print('\nTool calls:');print(json.dumps(s['events'],indent=2))
    def select(*_):
        l=next(l for l in lessons if l['id']==choose.value);task.value=l['prompt']
        with intro:
            clear_output();print(l['scenario']);print('\n'+'\n'.join(l['steps']))
            if l['mode']=='mcp':print('\nOpen the connected lab: https://colab.research.google.com/github/FeikoWielsma/Using-AI-Agents/blob/main/notebooks/demo39-MCP_Connected_Services.ipynb')
        run.disabled=l['mode']=='mcp';render()
    def execute(_):
        run.disabled=True
        try:
            l=next(l for l in lessons if l['id']==choose.value)
            runtime.run(client,'qwen3.8-max',states[choose.value],l['mode'],task.value,{'enable_thinking':False},team=team.value,specialist=specialist.value,discount=discount.value)
            render()
        except Exception as exc:
            with output:print(type(exc).__name__+': the run could not finish. Check access and retry.')
        finally:run.disabled=False
    def decision(approved):
        s=states[choose.value]
        if s['pending']:s['answer']=runtime.review(s,s['pending']['id'],approved);render()
    def save(_):
        from google.colab import files
        for name,data in states[choose.value]['artifacts'].items():
            path=Path('/content')/name;path.write_bytes(base64.b64decode(data));files.download(str(path))
    def clear(_):states[choose.value]=runtime.initial();render()
    def limit(_):
        try:runtime.call_tool(states[4],'guardrails','propose_refund',{'amount':80,'reason':'Boundary demonstration'})
        except ValueError:
            with output:print('Tool-level boundary: EUR 80 rejected by code. No refund recorded.')
    run.on_click(execute);reset.on_click(clear);download.on_click(save);boundary.on_click(limit)
    approve.on_click(lambda _:decision(True));reject.on_click(lambda _:decision(False));choose.observe(select,names='value')
    display(w.VBox([choose,intro,task,team,specialist,discount,w.HBox([run,reset,download]),w.HBox([approve,reject,boundary]),output]));select()

def show_demos(client,demos):
    import ipywidgets as w
    from IPython.display import display,clear_output
    selector=w.Dropdown(options=[(f'D{d["id"]:02} '+d['title'],d['id']) for d in demos],layout=w.Layout(width='95%'))
    run=w.Button(description='Run selected demo');output=w.Output()
    state=runtime.initial()
    def execute(_):
        d=next(d for d in demos if d['id']==selector.value)
        with output:
            clear_output();print(d['title']+'\n'+d['prompt']+'\nEnvironment: '+d['environment'])
            if d['id']==17:
                first=runtime.run_loop(client,'qwen3.8-max',runtime.initial(),'team','Suggest a three-item cafe menu for 20 visitors. Use the catalogue.',{'enable_thinking':False},role='Creative specialist.')
                print('\nFirst agent:\n'+first['answer'])
                second=runtime.run_loop(client,'qwen3.8-max',runtime.initial(),'team','Cost this menu for 20 visitors within EUR 100: '+first['answer'],{'enable_thinking':False},role='Operations specialist.')
                print('\nSecond agent receives the first result:\n'+second['answer'])
            elif d['id']==25:
                try:runtime.call_tool(runtime.initial(),'guardrails','propose_refund',dict(amount=80,reason='Boundary demo'))
                except ValueError as exc:print('Direct tool result:',str(exc),'\nNo model call or refund.')
            elif d['id']==28:
                s=runtime.initial();runtime.call_tool(s,'guardrails','propose_refund',dict(amount=40,reason='Review demo'));pid=s['pending']['id']
                print('Prepared proposal:',s['pending']);runtime.review(s,pid,False)
                try:runtime.review(s,pid,True)
                except ValueError as exc:print('Old approval rejected:',str(exc),'Ledger:',s['ledger'])
            elif d['environment']=='lab':
                mode={1:'tools',3:'team',4:'guardrails',5:'harness'}[d['module']]
                runtime.run(client,'qwen3.8-max',state,mode,d['prompt'],{'enable_thinking':False},specialist='accessibility' if d['id']==16 else 'operations',discount=d['id']==33)
                print(state['answer']);print('Tool calls:',json.dumps(state['events'],indent=2))
                for agent in state['agents']:print(agent['role']+':\n'+agent['answer'])
                if state['pending']:print('Pending proposal: use the main lab review controls for the full approval activity.')
                if state['comparison']:print('Browser comparison data:',state['comparison'])
            else:print('Use the named trainer environment or Connected services. No student installation.\nStop when: '+d['stop'])
    def wrapped(_):
        run.disabled=True
        try:execute(_)
        except Exception as exc:
            with output:print(type(exc).__name__+': demo could not finish. Use the main lab or the labelled fallback.')
        finally:run.disabled=False
    run.on_click(wrapped);display(w.VBox([selector,run,output]))

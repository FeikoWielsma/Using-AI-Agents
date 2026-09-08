"""Fictional café economy and agent tools. Money is integer cents; no real purchases."""
import copy
import json
import time
import uuid
from exploration_runtime import schema

SUPPLIER={'wrap':50,'falafel':120,'cheese':70,'fruit':80,'coffee':60,'milk':50,'oat_milk':80}
RECIPES={
 'falafel_wrap':dict(name='Falafel wrap',ingredients={'wrap':1,'falafel':1},allergens=['gluten'],vegan=True,minutes=3),
 'cheese_wrap':dict(name='Cheese toastie',ingredients={'wrap':1,'cheese':1},allergens=['gluten','milk'],vegan=False,minutes=3),
 'fruit_cup':dict(name='Fruit cup',ingredients={'fruit':1},allergens=[],vegan=True,minutes=1),
 'espresso':dict(name='Espresso',ingredients={'coffee':1},allergens=[],vegan=True,minutes=1),
 'latte':dict(name='Latte',ingredients={'coffee':1,'milk':1},allergens=['milk'],vegan=False,minutes=2),
 'oat_latte':dict(name='Oat latte',ingredients={'coffee':1,'oat_milk':1},allergens=['oats'],vegan=True,minutes=2)}

def initial():
 return dict(name='Your pop-up café',tagline='A small menu. A big idea.',theme='terracotta',menu=[],stock={k:0 for k in SUPPLIER},cash=10000,spent=0,revenue=0,pending=None,purchases=[],open=False,checks=None,orders=[],rushes=0,surprise=None,turns=[],answer='',history=[],tool_limit=12)

def prices(s):return {k:round(v*(1.5 if s['surprise']=='prices' else 1)) for k,v in SUPPLIER.items()}
def availability(s):return [k for k in SUPPLIER if not(s['surprise']=='delivery' and k=='oat_milk')]
def integer(n,lo,hi):
 if type(n) is not int or not lo<=n<=hi:raise ValueError(f'Use a whole number from {lo} to {hi}.')
 return n
def text(value,limit):
 if not isinstance(value,str) or not value.strip() or len(value)>limit:raise ValueError(f'Enter text under {limit+1} characters.')
 return value.strip()
def cost(s,recipe):return sum(prices(s)[k]*v for k,v in RECIPES[recipe]['ingredients'].items())
def portions(s,recipe):return min(s['stock'][k]//v for k,v in RECIPES[recipe]['ingredients'].items())
def check(s):
 rows=[dict(name='Three menu items',passed=len(s['menu'])==3),dict(name='Every item has stock',passed=bool(s['menu']) and all(portions(s,m['recipe'])>0 for m in s['menu'])),dict(name='At least one vegan option',passed=any(RECIPES[m['recipe']]['vegan'] for m in s['menu'])),dict(name='Prices cover ingredient costs',passed=bool(s['menu']) and all(m['price']>cost(s,m['recipe']) for m in s['menu']))]
 return dict(passed=all(r['passed'] for r in rows),checks=rows,note='Server checks of menu, stock and checkout rules; this does not run a browser.')
def view(s):
 result=copy.deepcopy(s);result['prices']=prices(s);result['available']=availability(s);result['recipes']=RECIPES;result['checks_now']=check(s)
 result['menu']=[dict(**m,**RECIPES[m['recipe']],portions=portions(s,m['recipe']),cost=cost(s,m['recipe'])) for m in s['menu']]
 result['waste_value']=sum(s['stock'][k]*prices(s)[k] for k in SUPPLIER)
 return result

TOOLS=[schema('inspect_cafe','Read the café, full recipes, stock, budget, orders and current constraints.'),
 schema('query_supplier','Read supplier prices and availability through the connected course MCP service. No purchase is made.'),
 schema('set_menu','Set exactly three recipe items. Prices are integer cents. Allergens and vegan labels come from recipes and cannot be overridden.',{'items':{'type':'array','minItems':3,'maxItems':3,'items':{'type':'object','properties':{'recipe':{'type':'string','enum':list(RECIPES)},'price':{'type':'integer','minimum':100,'maximum':1500}},'required':['recipe','price'],'additionalProperties':False}}},['items']),
 schema('propose_purchase','Propose ingredient quantities for human approval. No stock or money changes until approved.',{'quantities':{'type':'object','properties':{k:{'type':'integer','minimum':1,'maximum':40} for k in SUPPLIER},'additionalProperties':False}},['quantities']),
 schema('design_storefront','Change the café name, tagline and visual theme. The storefront is a working template, not arbitrary generated code.',{'name':{'type':'string'},'tagline':{'type':'string'},'theme':{'type':'string','enum':['terracotta','forest','midnight']}},['name','tagline','theme']),
 schema('test_checkout','Run server-side checkout checks for stock, margins, menu size and vegan choice. Reports failures; cannot open the café.')]

def context(s):return {k:v for k,v in view(s).items() if k not in ('turns','history','answer','busy')}

def call(s,name,args,supplier):
 if name=='inspect_cafe':return context(s)
 if name=='query_supplier':return dict(mcp=supplier(),effective_prices_cents=prices(s),available=availability(s),delivery='Before opening; approved orders arrive immediately in this simulation.')
 if name=='set_menu':
  items=args['items']
  if not isinstance(items,list) or len(items)!=3 or any(not isinstance(m,dict) or m.get('recipe') not in RECIPES for m in items) or len({m['recipe'] for m in items})!=3:raise ValueError('Choose three different catalogue recipes.')
  menu=[dict(recipe=m['recipe'],price=integer(m['price'],100,1500)) for m in items]
  if any(m['price']<=cost(s,m['recipe']) for m in menu):raise ValueError('Each price must exceed its ingredient cost.')
  s.update(menu=menu,open=False,checks=None);return dict(menu=menu,note='Menu saved. Human approval is required to open.')
 if name=='propose_purchase':
  if s['pending']:raise ValueError('Review the existing purchase before proposing another.')
  quantities=args['quantities']
  if not isinstance(quantities,dict) or not quantities or any(k not in availability(s) for k in quantities):raise ValueError('Choose available supplier ingredients.')
  quantities={k:integer(v,1,40) for k,v in quantities.items()};quote=prices(s);total=sum(quote[k]*v for k,v in quantities.items())
  if total>s['cash']:raise ValueError('The purchase exceeds the remaining cash budget.')
  s['pending']=dict(id=uuid.uuid4().hex,quantities=quantities,prices={k:quote[k] for k in quantities},total=total)
  return dict(proposal=s['pending'],status='Awaiting human approval; no purchase made.')
 if name=='design_storefront':
  if args['theme'] not in ['terracotta','forest','midnight']:raise ValueError('Choose a listed theme.')
  name=text(args['name'],50);tagline=text(args['tagline'],140)
  s.update(name=name,tagline=tagline,theme=args['theme'],open=False);return dict(name=name,theme=s['theme'],status='Preview updated. Human approval required to open.')
 if name=='test_checkout':s['checks']=check(s);return s['checks']
 raise ValueError('Tool unavailable.')

def order(s,recipe,budget=1500,vegan=False,allergy=None,customer='You',capacity=1000):
 if not s['open']:raise ValueError('Open the café before accepting orders.')
 item=next((m for m in s['menu'] if m['recipe']==recipe),None);r=RECIPES.get(recipe)
 reason=('Not on the menu' if not item else 'Over budget' if item['price']>budget else 'Dietary requirement' if (vegan and not r['vegan']) or allergy in r['allergens'] else 'Sold out' if portions(s,recipe)<1 else 'Kitchen at capacity' if r['minutes']>capacity else None)
 result=dict(customer=customer,recipe=recipe,status='missed' if reason else 'served',reason=reason,paid=0)
 if not reason:
  for k,v in r['ingredients'].items():s['stock'][k]-=v
  s['cash']+=item['price'];s['revenue']+=item['price'];result['paid']=item['price'];result['minutes']=r['minutes']
 s['orders'].append(result);return result

def action(s,data):
 name=data.get('action')
 if name=='approve_purchase':
  p=s['pending']
  if not p or p['id']!=data.get('id'):raise ValueError('This purchase is no longer awaiting approval.')
  if any(k not in availability(s) or prices(s)[k]!=p['prices'][k] for k in p['quantities']):raise ValueError('Supplier conditions changed. Reject this proposal and request a new quote.')
  if p['total']>s['cash']:raise ValueError('Insufficient cash.')
  for k,v in p['quantities'].items():s['stock'][k]+=v
  s['cash']-=p['total'];s['spent']+=p['total'];s['purchases'].append(p);s['pending']=None
 elif name=='reject_purchase':
  if not s['pending'] or s['pending']['id']!=data.get('id'):raise ValueError('This purchase is no longer awaiting approval.')
  s['pending']=None
 elif name=='open':
  if not check(s)['passed']:raise ValueError('Resolve the checkout checks before opening.')
  s['open']=True
 elif name=='order':order(s,data.get('recipe'))
 elif name=='surprise':
  if s['surprise']:raise ValueError('One surprise per café. Reset to try another.')
  if data.get('kind') not in ['delivery','vegan','prices']:raise ValueError('Choose a listed surprise.')
  s['surprise']=data['kind'];s['open']=False
 elif name=='rush':
  if not s['open']:raise ValueError('Open the café first.')
  if s['rushes']>=3:raise ValueError('Three lunch rushes completed. Reset to start a new café.')
  capacity=30
  for i in range(12):
   vegan=s['surprise']=='vegan' or i%3==0;allergy='milk' if i%4==0 else None;budget=400 if i%2 else 650
   suitable=[m for m in s['menu'] if m['price']<=budget and (not vegan or RECIPES[m['recipe']]['vegan']) and allergy not in RECIPES[m['recipe']]['allergens'] and portions(s,m['recipe'])>0]
   chosen=(suitable or s['menu'])[i%len(suitable or s['menu'])]
   result=order(s,chosen['recipe'],budget,vegan,allergy,f'Rush {s["rushes"]+1} · Customer {i+1}',capacity);capacity-=result.get('minutes',0)
  s['rushes']+=1
 else:raise ValueError('Unknown café action.')

def run(client,model,s,prompt,limit,team,supplier,emit,extra):
 s['turns']=[];s['tool_limit']=limit;start=time.monotonic()
 roles=['Menu designer','Operations specialist','Storefront builder'] if team else ['Café agent']
 instructions={'Menu designer':'Choose the concept and set three menu items. Do not purchase or design the storefront.', 'Operations specialist':'Query the supplier and propose stock for the menu for 12 customers. Do not change the menu or storefront. Stop for human approval.', 'Storefront builder':'Design the storefront and run checkout checks. Do not change the menu or propose purchases.'}
 scopes={'Menu designer':['inspect_cafe','set_menu'],'Operations specialist':['inspect_cafe','query_supplier','propose_purchase'],'Storefront builder':['inspect_cafe','design_storefront','test_checkout']}
 answers=[]
 for role in roles:
  allowed=[t for t in TOOLS if t['function']['name'] in scopes.get(role,[t['function']['name'] for t in TOOLS])]
  messages=[dict(role='system',content='You operate a fictional pop-up café. All prices are cents. Use tools to implement the request, not just describe a plan. Never claim purchases or opening are approved. You have '+str(limit)+' tool calls. '+instructions.get(role,'Prepare a concept, three menu items, one purchase proposal and storefront. Test checkout; missing stock needs human approval.')+' Current café: '+json.dumps(context(s))),dict(role='user',content=prompt)]
  count=0
  for turn in range(8):
   if time.monotonic()-start>210:answers.append(role+': Time limit reached.');break
   step=dict(agent=role,number=turn+1,status='waiting',tools=[],message='');s['turns'].append(step);emit(copy.deepcopy(step))
   result=client.chat.completions.create(model=model,messages=messages,tools=allowed,max_tokens=1400,extra_body=extra)
   msg=result.choices[0].message;step['message']=msg.content or ''
   if not msg.tool_calls:step['status']='answer';emit(copy.deepcopy(step));answers.append(role+': '+step['message']);break
   messages.append(msg.model_dump(exclude_none=True))
   for tc in msg.tool_calls:
    if count>=limit:break
    count+=1;entry=dict(tool=tc.function.name,arguments=tc.function.arguments,status='running');step['tools'].append(entry);step['status']='tools';emit(copy.deepcopy(step))
    try:
     args=json.loads(tc.function.arguments)
     if tc.function.name not in [t['function']['name'] for t in allowed]:raise ValueError('Tool unavailable to this specialist.')
     output=call(s,tc.function.name,args,supplier);entry['arguments']=args
    except (ValueError,KeyError,TypeError) as exc:output={'error':str(exc)}
    entry.update(result=output,status='error' if 'error' in output else 'done');emit(copy.deepcopy(step))
    messages.append(dict(role='tool',tool_call_id=tc.id,content=json.dumps(output)))
   step['status']='limit' if count>=limit or turn==7 else 'done';emit(copy.deepcopy(step))
   if step['status']=='limit':answers.append(role+': Run limit reached. Inspect the changes.');break
 s['answer']='\n\n'.join(answers);s['seconds']=round(time.monotonic()-start,1)
 s['history']=(s.get('history',[])+[dict(prompt=prompt,answer=s['answer'])])[-5:]

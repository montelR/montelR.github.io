// Fictional educational fixtures, not model outputs or production data.
export function fixtures({second=false, low=false, wrong=false, effect=false, suppress=false} = {}) {
  const cases = Array.from({length:5}, (_,i)=>({
    id:'repeat-'+(i+1), mechanism:'Stale preview', eligible:true,
    expectedA:'review', observedA:'review', expectedB:'ready', observedB:'ready',
    before:low?10:1, after:low?9:0, effects:0
  }));
  if(second) cases.push({...cases[0],id:'duplicate-schedule',mechanism:'Duplicate scheduling'});
  cases.push({id:'new-content',mechanism:'Necessary review',eligible:false,expectedA:'review',observedA:'review',expectedB:'review',observedB:'review',before:1,after:suppress?0:1,effects:0},
    {id:'invalid-state',mechanism:'Invalid state',eligible:false,expectedA:'blocked',observedA:'blocked',expectedB:'blocked',observedB:'blocked',before:0,after:0,effects:0});
  if(wrong) cases[0].observedB='blocked';
  if(effect) cases[0].effects=1;
  return cases;
}
export function evaluate(cases) {
  if(!cases.length || new Set(cases.map(c=>c.id)).size!==cases.length ||
    cases.some(c=>!c.id||!c.mechanism||![c.before,c.after,c.effects].every(v=>Number.isSafeInteger(v)&&v>=0))) throw new Error('Invalid paired cases');
  let correct=0,before=0,after=0,effects=0,necessary=true;
  const totals=new Map();
  for(const c of cases){
    correct+=Number(c.expectedA===c.observedA)+Number(c.expectedB===c.observedB);
    effects+=c.effects;
    if(c.eligible){
      before+=c.before; after+=c.after;
      totals.set(c.mechanism,(totals.get(c.mechanism)||0)+c.before-c.after);
    }else if(c.before!==c.after) necessary=false;
  }
  const total=cases.length*2, mechanisms=[...totals.values()].filter(v=>v>0).length;
  const reduction=before?(before-after)/before:null;
  const checks=[
    {label:'All outcomes match expected results',ok:correct===total,safety:true},
    {label:'Zero unauthorized effects',ok:effects===0,safety:true},
    {label:'Necessary review notices preserved',ok:necessary,safety:true},
    {label:'At least 25% eligible notice reduction',ok:before>0&&4*(before-after)>=before,safety:false},
    {label:'At least two independently defined improving mechanisms',ok:mechanisms>=2,safety:false}
  ];
  const verdict=checks.some(c=>c.safety&&!c.ok)?'FAIL':checks.some(c=>!c.ok)?'HOLD':'PASS';
  return {correct,total,before,after,effects,mechanisms,reduction,checks,verdict};
}

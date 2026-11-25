import {test} from 'node:test';
import assert from 'node:assert/strict';
import {fixtures,evaluate} from '../src/lib/evaluation.mjs';

test('all 32 condition combinations obey the predeclared gate',()=>{
  for(let n=0;n<32;n++){
    const [second,low,wrong,effect,suppress]=Array.from({length:5},(_,i)=>Boolean(n&(1<<i)));
    const cases=fixtures({second,low,wrong,effect,suppress});
    const r=evaluate(cases);
    assert.equal(r.total,second?16:14);
    assert.equal(r.correct,r.total-Number(wrong));
    assert.equal(r.reduction,low?.1:1);
    assert.equal(r.mechanisms,second?2:1);
    assert.equal(r.effects,Number(effect));
    assert.equal(r.verdict,wrong||effect||suppress?'FAIL':!second||low?'HOLD':'PASS');
  }
});
test('missing eligible denominator holds',()=>{
  assert.equal(evaluate(fixtures().filter(c=>!c.eligible)).verdict,'HOLD');
});
test('exact 25% threshold passes and lower threshold holds',()=>{
  const cases=fixtures({second:true}).map(c=>c.eligible?{...c,before:4,after:3}:c);
  assert.equal(evaluate(cases).verdict,'PASS');
  assert.equal(evaluate(cases.map(c=>c.eligible?{...c,before:5,after:4}:c)).verdict,'HOLD');
});
test('duplicate, empty and negative cases rejected',()=>{
  const cases=fixtures();
  assert.throws(()=>evaluate([]));
  assert.throws(()=>evaluate([...cases,cases[0]]));
  assert.throws(()=>evaluate([{...cases[0],after:-1}]));
});

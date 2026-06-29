const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_16x9";              // 10 x 5.625
p.author = "아파트 시그널맵";
p.title = "데이터로 내집마련하기";

// ---- palette ----
const NAVY="0F172A", SLATE="1E293B", MUT="64748B", LIGHT="F8FAFC", WHITE="FFFFFF";
const TEAL="0D9488", MINT="2DD4BF", BLUE="3B82F6", CORAL="F43F5E", AMBER="F59E0B", LINE="E2E8F0";
const HF="Cambria", BF="Calibri";
const W=10, H=5.625;
const sh=()=>({type:"outer",color:"000000",blur:9,offset:3,angle:90,opacity:0.12});

function bgDark(s){ s.background={color:NAVY}; }
function bgLight(s){ s.background={color:LIGHT}; }
function kicker(s,t,color){ s.addText(t,{x:0.6,y:0.42,w:9,h:0.3,fontFace:BF,fontSize:12,bold:true,color:color||TEAL,charSpacing:3,margin:0}); }
function title(s,t,color){ s.addText(t,{x:0.6,y:0.72,w:8.8,h:0.8,fontFace:HF,fontSize:30,bold:true,color:color||SLATE,margin:0}); }
function circleNum(s,n,x,y,color){ s.addShape(p.shapes.OVAL,{x,y,w:0.42,h:0.42,fill:{color}});
  s.addText(String(n),{x,y,w:0.42,h:0.42,align:"center",valign:"middle",fontFace:BF,fontSize:16,bold:true,color:WHITE,margin:0}); }
function card(s,x,y,w,h,fill){ s.addShape(p.shapes.ROUNDED_RECTANGLE,{x,y,w,h,rectRadius:0.08,fill:{color:fill||WHITE},line:{color:LINE,width:1},shadow:sh()}); }

// ===== Slide 1 — Title (dark) =====
let s=p.addSlide(); bgDark(s);
s.addText("DATA-DRIVEN HOME BUYING",{x:0.8,y:1.5,w:9,h:0.4,fontFace:BF,fontSize:13,bold:true,color:MINT,charSpacing:4,margin:0});
s.addText("데이터로 내집마련하기",{x:0.8,y:1.95,w:8.8,h:1.1,fontFace:HF,fontSize:48,bold:true,color:WHITE,margin:0});
s.addText("흩어진 부동산 데이터를 한 곳에 — 아파트 시그널맵",{x:0.8,y:3.05,w:8.8,h:0.5,fontFace:BF,fontSize:18,color:"CBD5E1",margin:0});
s.addShape(p.shapes.RECTANGLE,{x:0.82,y:3.75,w:0.5,h:0.05,fill:{color:MINT}});
s.addText("감으로 사는 부동산에서, 근거로 사는 부동산으로",{x:0.8,y:3.95,w:8.8,h:0.4,fontFace:BF,fontSize:13,italic:true,color:"94A3B8",margin:0});
s.addNotes("오프닝. '집은 인생에서 가장 큰 거래인데, 왜 우리는 감으로 살까?' 이 강의는 흩어진 부동산 데이터를 한 곳에 모아 근거로 판단하는 법을 다룬다.");

// ===== Slide 2 — Problem: scattered knowledge (light) =====
s=p.addSlide(); bgLight(s);
kicker(s,"왜 어려운가"); title(s,"부동산 공부가 어려운 진짜 이유");
s.addText("필요한 데이터가 5곳에 흩어져 있다",{x:0.6,y:1.48,w:9,h:0.4,fontFace:BF,fontSize:16,color:MUT,margin:0});
const srcs=[["KB 주간","매수심리·전세수급"],["국토부","실거래가·거래량"],["청약홈","분양가·청약일정"],["법원경매","낙찰가·수익률"],["네이버·호갱","급매 호가"]];
srcs.forEach((c,i)=>{ const x=0.6+i*1.84; card(s,x,2.05,1.66,1.5,WHITE);
  s.addText(c[0],{x:x,y:2.25,w:1.66,h:0.4,align:"center",fontFace:HF,fontSize:16,bold:true,color:TEAL,margin:0});
  s.addText(c[1],{x:x+0.08,y:2.7,w:1.5,h:0.7,align:"center",valign:"top",fontFace:BF,fontSize:11.5,color:SLATE,margin:0}); });
s.addText("↓  한 화면에서 자동 연결",{x:0.6,y:3.78,w:9,h:0.4,align:"center",fontFace:BF,fontSize:14,bold:true,color:CORAL,margin:0});
s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:2.7,y:4.25,w:4.6,h:0.85,rectRadius:0.1,fill:{color:NAVY},shadow:sh()});
s.addText("아파트 시그널맵",{x:2.7,y:4.32,w:4.6,h:0.45,align:"center",fontFace:HF,fontSize:20,bold:true,color:WHITE,margin:0});
s.addText("5개 공공·시장 데이터를 한 곳에서 해석",{x:2.7,y:4.77,w:4.6,h:0.3,align:"center",fontFace:BF,fontSize:11,color:MINT,margin:0});
s.addNotes("핵심 통증: 지식이 흩어져 있어서 초보자는 어디서 뭘 봐야 할지 모른다. 시그널맵은 이 5개를 한 곳에 모은다.");

// ===== Slide 3 — Real estate is a cycle (light) =====
s=p.addSlide(); bgLight(s);
kicker(s,"제1원리"); title(s,"부동산은 사이클이다");
const cx=3.0, cy=3.45, r=1.35;
s.addShape(p.shapes.OVAL,{x:cx-0.95,y:cy-0.55,w:1.9,h:1.1,fill:{color:NAVY}});
s.addText("부동산\n사이클",{x:cx-0.95,y:cy-0.55,w:1.9,h:1.1,align:"center",valign:"middle",fontFace:HF,fontSize:15,bold:true,color:WHITE,margin:0});
const phases=[["① 회복기","거래량 ↑ 먼저","매수 기회",TEAL,cx-0.55,cy-r-0.35],["② 상승기","가격 급등·과열",">",CORAL,cx+r-0.05,cy-0.35],["③ 후퇴기","거래량 ↓ 먼저","매도 신호",AMBER,cx-0.55,cy+r-0.45],["④ 침체기","바닥·급매 출현","",BLUE,cx-r-1.55,cy-0.35]];
phases.forEach(ph=>{ card(s,ph[4],ph[5],1.55,0.82,WHITE);
  s.addText(ph[0],{x:ph[4],y:ph[5]+0.08,w:1.55,h:0.32,align:"center",fontFace:HF,fontSize:13,bold:true,color:ph[3],margin:0});
  s.addText(ph[1],{x:ph[4],y:ph[5]+0.42,w:1.55,h:0.32,align:"center",fontFace:BF,fontSize:10.5,color:SLATE,margin:0}); });
card(s,6.55,1.95,3.0,3.0,WHITE);
s.addText("핵심 통찰",{x:6.75,y:2.12,w:2.6,h:0.35,fontFace:HF,fontSize:15,bold:true,color:TEAL,margin:0});
s.addText([
 {text:"가격보다 거래량과 심리가 ",options:{}},{text:"먼저",options:{bold:true,color:CORAL}},{text:" 움직인다.",options:{breakLine:true}},
 {text:"",options:{breakLine:true}},
 {text:"그래서 가격만 보면 늦는다. 시그널맵은 ",options:{}},{text:"전세수급·매수심리·거래량",options:{bold:true,color:TEAL}},{text:"을 함께 본다.",options:{}},
],{x:6.75,y:2.55,w:2.65,h:2.2,fontFace:BF,fontSize:13.5,color:SLATE,lineSpacingMultiple:1.15,margin:0});
s.addNotes("4국면을 시계방향으로. 회복기에 거래량이 먼저 살아나고, 후퇴기에 거래량이 먼저 마른다. 가격은 후행한다.");

// ===== Slide 4 — 4 engines (light) =====
s=p.addSlide(); bgLight(s);
kicker(s,"무엇이 사이클을 움직이나"); title(s,"사이클을 움직이는 4개의 엔진");
const eng=[["유동성 (돈)",BLUE,"금리가 낮으면 돈이 부동산으로. 기준금리↓ → 대출↑ → 매수↑"],
 ["전세",TEAL,"전세가 마르면(전세난) 세입자가 '차라리 사자'로 전환 → 매매 압력"],
 ["공급 (입주물량)",AMBER,"입주 폭탄은 가격을 누르고, 공급 가뭄은 가격을 띄운다"],
 ["심리",CORAL,"매수자가 많아지면(매수우위) 호가가 오르고 추격매수가 붙는다"]];
eng.forEach((e,i)=>{ const x=0.6+(i%2)*4.65, y=1.7+Math.floor(i/2)*1.78;
  card(s,x,y,4.4,1.6,WHITE); circleNum(s,i+1,x+0.25,y+0.28,e[1]);
  s.addText(e[0],{x:x+0.85,y:y+0.28,w:3.3,h:0.45,fontFace:HF,fontSize:17,bold:true,color:e[1],valign:"middle",margin:0});
  s.addText(e[2],{x:x+0.3,y:y+0.82,w:3.9,h:0.65,fontFace:BF,fontSize:12.5,color:SLATE,margin:0,lineSpacingMultiple:1.05}); });
s.addNotes("이 4개가 서로 맞물려 사이클을 만든다. 시그널맵의 지표들은 전부 이 4엔진을 수치화한 것.");

// ===== Slide 5 — flow of indicators (light) =====
s=p.addSlide(); bgLight(s);
kicker(s,"지표 읽기 ①"); title(s,"지표는 순서대로 연결된다");
const flow=[["전세수급",TEAL,"전세가 마른다"],["매수심리",BLUE,"사자가 많아진다"],["거래량",AMBER,"거래가 늘어난다"],["매매가격",CORAL,"가격이 오른다"]];
flow.forEach((f,i)=>{ const x=0.55+i*2.4; card(s,x,2.1,2.0,1.5,WHITE);
  s.addText(f[0],{x:x,y:2.35,w:2.0,h:0.45,align:"center",fontFace:HF,fontSize:18,bold:true,color:f[1],margin:0});
  s.addText(f[2],{x:x,y:2.85,w:2.0,h:0.6,align:"center",valign:"top",fontFace:BF,fontSize:12,color:SLATE,margin:0});
  if(i<3) s.addText("→",{x:x+1.98,y:2.1,w:0.45,h:1.5,align:"center",valign:"middle",fontFace:BF,fontSize:24,bold:true,color:MUT,margin:0}); });
s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:0.55,y:3.95,w:8.85,h:1.05,rectRadius:0.08,fill:{color:"ECFDF5"},line:{color:MINT,width:1}});
s.addText([{text:"실거주 수요(전세)가 압력솥처럼 차오르면 → 매매로 분출한다. ",options:{}},
 {text:"전세는 투기 수요가 거의 없어, 그 지역에 '진짜 살려는 사람'의 압력을 보여준다.",options:{bold:true,color:TEAL}}],
 {x:0.85,y:4.12,w:8.3,h:0.75,fontFace:BF,fontSize:13.5,color:SLATE,valign:"middle",margin:0,lineSpacingMultiple:1.1});
s.addNotes("전세수급 → 매수심리 → 거래량 → 가격. 이 연결고리를 이해하면 가격이 오르기 전에 신호를 잡을 수 있다.");

// ===== Slide 6 — threshold reading (light) =====
s=p.addSlide(); bgLight(s);
kicker(s,"지표 읽기 ②"); title(s,"임계 구간이 행동을 바꾼다");
card(s,0.6,1.7,4.4,3.3,WHITE);
s.addText("전세수급지수",{x:0.85,y:1.9,w:4,h:0.4,fontFace:HF,fontSize:17,bold:true,color:TEAL,margin:0});
const js=[["~80","공급우위 · 역전세 위험",MUT],["80~120","수급 균형",SLATE],["120~150","타이트 · 매매 고민 시작",AMBER],["150~180","전세난 · 매매 전환 본격",CORAL],["180~","매매 끌어올림 (상승기)",CORAL]];
js.forEach((r,i)=>{ const y=2.4+i*0.5; s.addText(r[0],{x:0.85,y:y,w:1.0,h:0.4,fontFace:BF,fontSize:13,bold:true,color:r[2],valign:"middle",margin:0});
  s.addText(r[1],{x:1.95,y:y,w:2.95,h:0.4,fontFace:BF,fontSize:12,color:SLATE,valign:"middle",margin:0}); });
card(s,5.25,1.7,4.15,3.3,WHITE);
s.addText("매수우위지수",{x:5.5,y:1.9,w:3.6,h:0.4,fontFace:HF,fontSize:17,bold:true,color:BLUE,margin:0});
const bs=[["~40","매수자 우위 · 급매 출현 (기회!)",TEAL],["40~100","심리 회복 ~ 균형",SLATE],["100~","매도자 우위 · FOMO 임계",CORAL]];
bs.forEach((r,i)=>{ const y=2.45+i*0.62; s.addText(r[0],{x:5.5,y:y,w:1.0,h:0.5,fontFace:BF,fontSize:13,bold:true,color:r[2],valign:"middle",margin:0});
  s.addText(r[1],{x:6.55,y:y,w:2.7,h:0.5,fontFace:BF,fontSize:12,color:SLATE,valign:"middle",margin:0}); });
s.addText([{text:"역발상: ",options:{bold:true,color:CORAL}},{text:"매수심리 40 이하(공포 구간)가 오히려 매수 적기인 경우가 많다.",options:{}}],
 {x:5.5,y:4.42,w:3.7,h:0.5,fontFace:BF,fontSize:11.5,italic:true,color:SLATE,valign:"middle",margin:0});
s.addNotes("숫자보다 '이 구간을 넘으면 사람들이 어떻게 행동하나'가 핵심. 150 돌파=전세난, 100 돌파=FOMO.");

// ===== Slide 7 — two grade axes + undervaluation (light) =====
s=p.addSlide(); bgLight(s);
kicker(s,"지표 읽기 ③"); title(s,"급지 — 두 개의 좌표축");
card(s,0.6,1.7,4.4,2.0,WHITE);
s.addText("지역 급지  A~D",{x:0.85,y:1.88,w:4,h:0.4,fontFace:HF,fontSize:16,bold:true,color:BLUE,margin:0});
s.addText([{text:"시군구 단위. ",options:{bold:true}},{text:"이 동네가 수도권에서 어느 계급인가.",options:{breakLine:true}},
 {text:"A = 상위 동네(강남) · D = 외곽",options:{color:MUT}}],{x:0.85,y:2.35,w:3.9,h:1.2,fontFace:BF,fontSize:13,color:SLATE,margin:0,lineSpacingMultiple:1.1});
card(s,5.25,1.7,4.15,2.0,WHITE);
s.addText("단지 급지  1~5",{x:5.5,y:1.88,w:3.6,h:0.4,fontFace:HF,fontSize:16,bold:true,color:TEAL,margin:0});
s.addText([{text:"단지 단위. ",options:{bold:true}},{text:"그 동네 안에서 대장이냐 막내냐.",options:{breakLine:true}},
 {text:"1 = 동네 내 최상위 · 5 = 하위",options:{color:MUT}}],{x:5.5,y:2.35,w:3.6,h:1.2,fontFace:BF,fontSize:13,color:SLATE,margin:0,lineSpacingMultiple:1.1});
s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:0.6,y:3.95,w:8.8,h:1.05,rectRadius:0.08,fill:{color:NAVY},shadow:sh()});
s.addText([{text:"저평가도 ",options:{bold:true,color:MINT}},{text:"= 입지(교통·학원·환경)가 매기는 적정가 vs 실제 시장가. ",options:{color:WHITE}},
 {text:"시장이 아직 못 알아본 입지를 데이터가 먼저 찾는다.",options:{bold:true,color:MINT}}],
 {x:0.9,y:4.12,w:8.2,h:0.75,fontFace:BF,fontSize:13.5,color:WHITE,valign:"middle",margin:0,lineSpacingMultiple:1.1});
s.addNotes("두 급지는 직교한다. D지역 1급지(외곽 대장)와 A지역 5급지(강남 막내)는 전혀 다른 투자.");

// ===== Slide 8 — signal logic buy vs sell (light) =====
s=p.addSlide(); bgLight(s);
kicker(s,"종합"); title(s,"시그널은 이렇게 만들어진다");
card(s,0.6,1.7,4.4,3.3,"ECFDF5");
s.addText("매수 신호  STRONG BUY / BUY",{x:0.85,y:1.92,w:4,h:0.4,fontFace:HF,fontSize:16,bold:true,color:TEAL,margin:0});
s.addText([{text:"전세난 (전세수급 150↑)",options:{bullet:true,breakLine:true}},{text:"매수심리 회복 (매수우위 ↑)",options:{bullet:true,breakLine:true}},
 {text:"입주물량 부족 (공급 가뭄)",options:{bullet:true,breakLine:true}},{text:"거래량 회복",options:{bullet:true}}],
 {x:0.95,y:2.5,w:3.8,h:2.3,fontFace:BF,fontSize:14,color:SLATE,paraSpaceAfter:10,margin:0});
card(s,5.25,1.7,4.15,3.3,"FEF2F2");
s.addText("매도 신호  SELL RISK",{x:5.5,y:1.92,w:3.6,h:0.4,fontFace:HF,fontSize:16,bold:true,color:CORAL,margin:0});
s.addText([{text:"매매가격 하락 전환",options:{bullet:true,breakLine:true}},{text:"입주물량 과잉",options:{bullet:true,breakLine:true}},
 {text:"거래량 위축",options:{bullet:true,breakLine:true}},{text:"급지역전(끝물) — 하급지가 더 오름 + 금리 상승",options:{bullet:true}}],
 {x:5.6,y:2.5,w:3.6,h:2.3,fontFace:BF,fontSize:14,color:SLATE,paraSpaceAfter:10,margin:0});
s.addNotes("여러 조건이 겹칠수록 강한 신호. '지난 시그널' 백테스트로 과거 그 구간에 실제 가격이 올랐는지 검증할 수 있다.");

// ===== Slide 9 — 7 tabs = all in one place (light) — product hero =====
s=p.addSlide(); bgLight(s);
kicker(s,"제품"); title(s,"흩어진 데이터를 한 곳에 — 7개의 탭");
const tabs=[["시그널","사이클상 매수/매도 타이밍",TEAL],["저평가","입지 대비 싼 지역·단지",BLUE],["경매","시세 이하 낙찰 물건",AMBER],
 ["급매","시세 이하 호가 매물",CORAL],["청약","평형별 분양가·일정·메리트",TEAL],["재건축","잠재력·가치 ROI",BLUE]];
tabs.forEach((t,i)=>{ const x=0.6+(i%4)*2.28, y=1.75+Math.floor(i/4)*1.55;
  card(s,x,y,2.1,1.35,WHITE);
  s.addText(t[0],{x:x,y:y+0.16,w:2.1,h:0.4,align:"center",fontFace:HF,fontSize:16,bold:true,color:t[2],margin:0});
  s.addText(t[1],{x:x+0.1,y:y+0.6,w:1.9,h:0.65,align:"center",valign:"top",fontFace:BF,fontSize:11,color:SLATE,margin:0}); });
// 결론 = 모든 걸 종합하는 종착점 (넓은 hero 카드로 우하단 채움)
s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:5.16,y:3.3,w:4.38,h:1.35,rectRadius:0.08,fill:{color:NAVY},shadow:sh()});
s.addText("결론",{x:5.36,y:3.5,w:1.4,h:0.4,fontFace:HF,fontSize:18,bold:true,color:MINT,valign:"middle",margin:0});
s.addText("내 자본 → LTV·DSR → 매수가능가 → BUY+ × 저평가 × 단지급지로 종합 추천",
 {x:5.36,y:3.95,w:4.0,h:0.6,fontFace:BF,fontSize:11.5,color:WHITE,valign:"top",margin:0,lineSpacingMultiple:1.05});
s.addNotes("이 슬라이드가 제품의 힘. 흩어진 5개 데이터가 7개 탭으로 정리되고, 결론 탭에서 한 방에 종합된다.");

// ===== Slide 10 — practical roadmap (light) =====
s=p.addSlide(); bgLight(s);
kicker(s,"실전"); title(s,"이 순서로 내집을 찾는다");
const steps=[["사이클","시그널 탭 — 지금 상승/끝물?"],["지역","BUY+ × 저평가로 동네 압축"],["단지","단지급지로 알짜 단지 선별"],
 ["매물","경매·급매·청약에서 실물 발굴"],["자금","결론 탭 — LTV·DSR·취득세 반영"],["결정","모두 초록불이면 행동"]];
steps.forEach((st,i)=>{ const x=0.55+i*1.57; circleNum(s,i+1,x+0.5,1.95,i<5?TEAL:CORAL);
  card(s,x,2.6,1.42,1.7,WHITE);
  s.addText(st[0],{x:x,y:2.78,w:1.42,h:0.4,align:"center",fontFace:HF,fontSize:15,bold:true,color:SLATE,margin:0});
  s.addText(st[1],{x:x+0.08,y:3.2,w:1.26,h:1.0,align:"center",valign:"top",fontFace:BF,fontSize:10.5,color:MUT,margin:0,lineSpacingMultiple:1.05});
  if(i<5) s.addText("→",{x:x+1.4,y:2.6,w:0.2,h:1.7,align:"center",valign:"middle",fontFace:BF,fontSize:16,bold:true,color:LINE,margin:0}); });
s.addText("한 지역을 골라 1→6을 끝까지 돌려보면, 데이터로 내집을 고르는 감이 잡힌다.",{x:0.6,y:4.5,w:8.8,h:0.5,align:"center",fontFace:BF,fontSize:13,italic:true,color:TEAL,margin:0});
s.addNotes("강의 실습 시나리오. 한 지역으로 6단계를 시연하면 청중이 사용법을 체득한다.");

// ===== Slide 11 — closing (dark) =====
s=p.addSlide(); bgDark(s);
s.addText("THE PROMISE",{x:0.8,y:1.5,w:9,h:0.4,fontFace:BF,fontSize:13,bold:true,color:MINT,charSpacing:4,margin:0});
s.addText("산개된 부동산 지식을\n한 곳에 모았더니,",{x:0.8,y:1.95,w:8.8,h:1.4,fontFace:HF,fontSize:34,bold:true,color:WHITE,margin:0,lineSpacingMultiple:1.1});
s.addText("내집마련이 한 방에 풀렸다.",{x:0.8,y:3.35,w:8.8,h:0.7,fontFace:HF,fontSize:34,bold:true,color:MINT,margin:0});
s.addText("데이터로 내집마련하기  ·  아파트 시그널맵",{x:0.8,y:4.5,w:8.8,h:0.4,fontFace:BF,fontSize:14,color:"94A3B8",margin:0});
s.addNotes("클로징. 한 문장으로 정리: 흩어진 지식을 한 곳에 → 근거로 내집마련.");

p.writeFile({fileName:"/Users/ys.choi/dev-private/realty-signal-map/docs/데이터로_내집마련하기.pptx"}).then(f=>console.log("WROTE",f));

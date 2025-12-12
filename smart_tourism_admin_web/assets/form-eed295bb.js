import{f as o,H as L,e as z,I as O,bI as Y,G as se,d as le,h as me,L as fe,k as he,c4 as ge,K as xe,w as u,by as ye,bp as _e,bq as ze,c5 as ke,t as ie,n as j,c6 as k,q as Se,F as oe,c7 as ne,bB as we,bk as Z,X as E,bD as re,c8 as Ce,c9 as Ne,bR as Ie,au as Pe,a2 as Te,r as _,bS as $e,o as x,c as q,b as s,ab as n,R as t,bU as Re,a as i,ac as U,ca as Ue,a6 as ce,A as ee,bo as te,N as A,bX as de,aS as D,aa as ue,Q as $,a1 as R,a5 as F,ar as De,ah as pe,bW as Fe,b7 as Be}from"./index-5805bd08.js";import{A as qe}from"./ArrowBack-6aacbee0.js";import{g as Le}from"./Forward-dbe0c59b.js";import{N as Oe}from"./Form-9e4f5768.js";import{N as B}from"./FormItem-8b481c62.js";import{N as ve}from"./DatePicker-8deac17c.js";import{N as je}from"./Switch-1df89df0.js";import{N as Ae}from"./Space-a5c105a8.js";const Ee=o("steps",`
 width: 100%;
 display: flex;
`,[o("step",`
 position: relative;
 display: flex;
 flex: 1;
 `,[L("disabled","cursor: not-allowed"),L("clickable",`
 cursor: pointer;
 `),z("&:last-child",[o("step-splitor","display: none;")])]),o("step-splitor",`
 background-color: var(--n-splitor-color);
 margin-top: calc(var(--n-step-header-font-size) / 2);
 height: 1px;
 flex: 1;
 align-self: flex-start;
 margin-left: 12px;
 margin-right: 12px;
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `),o("step-content","flex: 1;",[o("step-content-header",`
 color: var(--n-header-text-color);
 margin-top: calc(var(--n-indicator-size) / 2 - var(--n-step-header-font-size) / 2);
 line-height: var(--n-step-header-font-size);
 font-size: var(--n-step-header-font-size);
 position: relative;
 display: flex;
 font-weight: var(--n-step-header-font-weight);
 margin-left: 9px;
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `,[O("title",`
 white-space: nowrap;
 flex: 0;
 `)]),O("description",`
 color: var(--n-description-text-color);
 margin-top: 12px;
 margin-left: 9px;
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `)]),o("step-indicator",`
 background-color: var(--n-indicator-color);
 box-shadow: 0 0 0 1px var(--n-indicator-border-color);
 height: var(--n-indicator-size);
 width: var(--n-indicator-size);
 border-radius: 50%;
 display: flex;
 align-items: center;
 justify-content: center;
 transition:
 background-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 `,[o("step-indicator-slot",`
 position: relative;
 width: var(--n-indicator-icon-size);
 height: var(--n-indicator-icon-size);
 font-size: var(--n-indicator-icon-size);
 line-height: var(--n-indicator-icon-size);
 `,[O("index",`
 display: inline-block;
 text-align: center;
 position: absolute;
 left: 0;
 top: 0;
 white-space: nowrap;
 font-size: var(--n-indicator-index-font-size);
 width: var(--n-indicator-icon-size);
 height: var(--n-indicator-icon-size);
 line-height: var(--n-indicator-icon-size);
 color: var(--n-indicator-text-color);
 transition: color .3s var(--n-bezier);
 `,[Y()]),o("icon",`
 color: var(--n-indicator-text-color);
 transition: color .3s var(--n-bezier);
 `,[Y()]),o("base-icon",`
 color: var(--n-indicator-text-color);
 transition: color .3s var(--n-bezier);
 `,[Y()])])]),L("vertical","flex-direction: column;",[se("show-description",[z(">",[o("step","padding-bottom: 8px;")])]),z(">",[o("step","margin-bottom: 16px;",[z("&:last-child","margin-bottom: 0;"),z(">",[o("step-indicator",[z(">",[o("step-splitor",`
 position: absolute;
 bottom: -8px;
 width: 1px;
 margin: 0 !important;
 left: calc(var(--n-indicator-size) / 2);
 height: calc(100% - var(--n-indicator-size));
 `)])]),o("step-content",[O("description","margin-top: 8px;")])])])])]),L("content-bottom",[se("vertical",[z(">",[o("step","flex-direction: column",[z(">",[o("step-line","display: flex;",[z(">",[o("step-splitor",`
 margin-top: 0;
 align-self: center;
 `)])])]),z(">",[o("step-content","margin-top: calc(var(--n-indicator-size) / 2 - var(--n-step-header-font-size) / 2);",[o("step-content-header",`
 margin-left: 0;
 `),o("step-content__description",`
 margin-left: 0;
 `)])])])])])])]);function Ve(e,b){return typeof e!="object"||e===null||Array.isArray(e)?null:(e.props||(e.props={}),e.props.internalIndex=b+1,e)}function Qe(e){return e.map((b,f)=>Ve(b,f))}const He=Object.assign(Object.assign({},he.props),{current:Number,status:{type:String,default:"process"},size:{type:String,default:"medium"},vertical:Boolean,contentPlacement:{type:String,default:"right"},"onUpdate:current":[Function,Array],onUpdateCurrent:[Function,Array]}),be=_e("n-steps"),Ke=le({name:"Steps",props:He,slots:Object,setup(e,{slots:b}){const{mergedClsPrefixRef:f,mergedRtlRef:p}=me(e),S=fe("Steps",p,f),w=he("Steps","-steps",Ee,ge,e,f);return xe(be,{props:e,mergedThemeRef:w,mergedClsPrefixRef:f,stepsSlots:b}),{mergedClsPrefix:f,rtlEnabled:S}},render(){const{mergedClsPrefix:e}=this;return u("div",{class:[`${e}-steps`,this.rtlEnabled&&`${e}-steps--rtl`,this.vertical&&`${e}-steps--vertical`,this.contentPlacement==="bottom"&&`${e}-steps--content-bottom`]},Qe(ye(Le(this))))}}),Me={status:String,title:String,description:String,disabled:Boolean,internalIndex:{type:Number,default:0}},ae=le({name:"Step",props:Me,slots:Object,setup(e){const b=ze(be,null);b||ke("step","`n-step` must be placed inside `n-steps`.");const{inlineThemeDisabled:f}=me(),{props:p,mergedThemeRef:S,mergedClsPrefixRef:w,stepsSlots:c}=b,C=ie(p,"vertical"),d=ie(p,"contentPlacement"),N=j(()=>{const{status:r}=e;if(r)return r;{const{internalIndex:m}=e,{current:P}=p;if(P===void 0)return"process";if(m<P)return"finish";if(m===P)return p.status||"process";if(m>P)return"wait"}return"process"}),I=j(()=>{const{value:r}=N,{size:m}=p,{common:{cubicBezierEaseInOut:P},self:{stepHeaderFontWeight:T,[k("stepHeaderFontSize",m)]:V,[k("indicatorIndexFontSize",m)]:Q,[k("indicatorSize",m)]:H,[k("indicatorIconSize",m)]:K,[k("indicatorTextColor",r)]:M,[k("indicatorBorderColor",r)]:W,[k("headerTextColor",r)]:X,[k("splitorColor",r)]:G,[k("indicatorColor",r)]:J,[k("descriptionTextColor",r)]:h}}=S.value;return{"--n-bezier":P,"--n-description-text-color":h,"--n-header-text-color":X,"--n-indicator-border-color":W,"--n-indicator-color":J,"--n-indicator-icon-size":K,"--n-indicator-index-font-size":Q,"--n-indicator-size":H,"--n-indicator-text-color":M,"--n-splitor-color":G,"--n-step-header-font-size":V,"--n-step-header-font-weight":T}}),v=f?Se("step",j(()=>{const{value:r}=N,{size:m}=p;return`${r[0]}${m[0]}`}),I,p):void 0,y=j(()=>{if(e.disabled)return;const{onUpdateCurrent:r,"onUpdate:current":m}=p;return r||m?()=>{r&&oe(r,e.internalIndex),m&&oe(m,e.internalIndex)}:void 0});return{stepsSlots:c,mergedClsPrefix:w,vertical:C,mergedStatus:N,handleStepClick:y,cssVars:f?void 0:I,themeClass:v==null?void 0:v.themeClass,onRender:v==null?void 0:v.onRender,contentPlacement:d}},render(){const{mergedClsPrefix:e,onRender:b,handleStepClick:f,disabled:p,contentPlacement:S,vertical:w}=this,c=ne(this.$slots.default,v=>{const y=v||this.description;return y?u("div",{class:`${e}-step-content__description`},y):null}),C=u("div",{class:`${e}-step-splitor`}),d=u("div",{class:`${e}-step-indicator`,key:S},u("div",{class:`${e}-step-indicator-slot`},u(we,null,{default:()=>ne(this.$slots.icon,v=>{const{mergedStatus:y,stepsSlots:r}=this;return y==="finish"||y==="error"?y==="finish"?u(re,{clsPrefix:e,key:"finish"},{default:()=>Z(r["finish-icon"],()=>[u(Ce,null)])}):y==="error"?u(re,{clsPrefix:e,key:"error"},{default:()=>Z(r["error-icon"],()=>[u(Ne,null)])}):null:v||u("div",{key:this.internalIndex,class:`${e}-step-indicator-slot__index`},this.internalIndex)})})),w?C:null),N=u("div",{class:`${e}-step-content`},u("div",{class:`${e}-step-content-header`},u("div",{class:`${e}-step-content-header__title`},Z(this.$slots.title,()=>[this.title])),!w&&S==="right"?C:null),c);let I;return!w&&S==="bottom"?I=u(E,null,u("div",{class:`${e}-step-line`},d,C),N):I=u(E,null,d,N),b==null||b(),u("div",{class:[`${e}-step`,p&&`${e}-step--disabled`,!p&&f&&`${e}-step--clickable`,this.themeClass,c&&`${e}-step--show-description`,`${e}-step--${this.mergedStatus}-status`],style:this.cssVars,onClick:f},I)}}),We={class:"activity-form-container"},Xe={class:"header-section"},Ge={class:"header-left"},Je={class:"header-title"},Ye={class:"steps-section"},Ze={class:"content-section"},et={class:"content-wrapper"},tt={class:"step-content"},at={class:"step-content"},lt={class:"template-fields"},st={class:"field-label"},it={class:"field-type"},ot={class:"field-actions"},nt={class:"add-field-button"},rt={class:"step-content"},ct={class:"coupon-table"},dt={class:"table-cell"},ut={class:"table-cell"},pt={class:"table-cell"},vt={class:"table-cell"},mt={class:"table-cell"},ht={class:"table-cell"},bt={class:"footer-actions"},ft=le({__name:"form",setup(e){const b=Ie(),f=Pe(),p=Te(),S=_(!!f.query.id),w=_(S.value?"编辑活动":"新增活动"),c=_(1),C=_(null),d=$e({activityName:"",totalQuota:null,maxPerPerson:null,ageLimit:null,memberThreshold:null,activityTime:null}),N=_([{label:"不限",value:"unlimited"},{label:"3-12岁",value:"3-12"},{label:"12-18岁",value:"12-18"},{label:"18-30岁",value:"18-30"},{label:"18-60岁",value:"18-60"},{label:"30-50岁",value:"30-50"}]),I=_([{label:"无限制",value:"unlimited"},{label:"等级1",value:"level1"},{label:"等级2",value:"level2"},{label:"等级3",value:"level3"},{label:"等级4",value:"level4"},{label:"等级5",value:"level5"}]),v=_([{id:1,label:"姓名",type:"text",required:!0,isDefault:!0},{id:2,label:"手机号",type:"text",required:!0,isDefault:!0},{id:3,label:"账号名称",type:"text",required:!0,isDefault:!0},{id:4,label:"备注",type:"richtext",required:!1,isDefault:!0}]),y=h=>{const a=v.value.length>0?Math.max(...v.value.map(g=>g.id))+1:1,l={text:"单文本",richtext:"富文本",select:"选择框",date:"日期框"};v.value.push({id:a,label:`${l[h]}字段${a}`,type:h,required:!1,isDefault:!1}),p.success("字段添加成功")},r=[{label:"单文本",key:"text"},{label:"富文本",key:"richtext"},{label:"选择框",key:"select"},{label:"日期框",key:"date"}],m=h=>{y(h)},P=h=>{v.value=v.value.filter(a=>a.id!==h),p.success("字段删除成功")},T=_([]),V=_([{label:"满减券",value:"cash"},{label:"折扣券",value:"discount"}]),Q=_([{label:"不限制",value:"unlimited"},{label:"美味餐厅",value:"merchant1"},{label:"舒适酒店",value:"merchant2"},{label:"欢乐KTV",value:"merchant3"},{label:"时尚购物中心",value:"merchant4"},{label:"咖啡时光",value:"merchant5"}]),H=_([{label:"餐饮类",value:"catering"},{label:"购物类",value:"shopping"},{label:"娱乐类",value:"entertainment"},{label:"住宿类",value:"accommodation"}]),K=()=>{const h=T.value.length>0?Math.max(...T.value.map(a=>a.id))+1:1;T.value.push({id:h,type:"",merchants:[],timeSlot:"",category:"",targetDistribution:!1})},M=h=>{T.value=T.value.filter(a=>a.id!==h)},W=()=>{b.back()},X=()=>{c.value>1&&c.value--},G=()=>{var h;c.value===1?(h=C.value)==null||h.validate(a=>{a||(c.value=2)}):c.value===2&&(c.value=3)},J=()=>{p.success("活动保存成功"),setTimeout(()=>{b.push("/activity")},1e3)};return(h,a)=>(x(),q("div",We,[s(t(Fe),{"has-sider":"",class:"h-full w-full"},{default:n(()=>[s(t(Re),{class:"h-full flex flex-col"},{default:n(()=>[i("div",Xe,[i("div",Ge,[s(t(U),{text:"",onClick:W,class:"back-button"},{icon:n(()=>[s(t(Ue),{size:"20"},{default:n(()=>[s(t(qe))]),_:1})]),_:1}),i("span",Je,ce(w.value),1)]),a[6]||(a[6]=i("div",{class:"header-placeholder"},null,-1))]),i("div",Ye,[s(t(Ke),{current:c.value,class:"steps-container"},{default:n(()=>[s(t(ae),{title:"活动信息"}),s(t(ae),{title:"报名模板配置"}),s(t(ae),{title:"优惠券配置"})]),_:1},8,["current"])]),i("div",Ze,[i("div",et,[ee(i("div",tt,[s(t(Oe),{ref_key:"activityFormRef",ref:C,model:d,rules:{activityName:{required:!0,message:"请输入活动名称",trigger:"blur"},totalQuota:{required:!0,message:"请输入总名额限制",trigger:"blur",type:"number"},maxPerPerson:{required:!0,message:"请输入单人最大报名数",trigger:"blur",type:"number"},ageLimit:{required:!0,message:"请选择年龄限制",trigger:"change"},memberThreshold:{required:!0,message:"请选择会员门槛",trigger:"change"},activityTime:{required:!0,message:"请选择活动时间",trigger:"change",type:"number"}},"label-placement":"left","label-width":"140px"},{default:n(()=>[s(t(B),{label:"活动名称",path:"activityName"},{default:n(()=>[s(t(A),{value:d.activityName,"onUpdate:value":a[0]||(a[0]=l=>d.activityName=l),placeholder:"请输入活动名称",clearable:""},null,8,["value"])]),_:1}),s(t(B),{label:"总名额限制",path:"totalQuota"},{default:n(()=>[s(t(de),{value:d.totalQuota,"onUpdate:value":a[1]||(a[1]=l=>d.totalQuota=l),placeholder:"请输入总名额限制",min:1,style:{width:"100%"}},null,8,["value"])]),_:1}),s(t(B),{label:"单人最大报名数",path:"maxPerPerson"},{default:n(()=>[s(t(de),{value:d.maxPerPerson,"onUpdate:value":a[2]||(a[2]=l=>d.maxPerPerson=l),placeholder:"请输入单人最大报名数",min:1,style:{width:"100%"}},null,8,["value"])]),_:1}),s(t(B),{label:"年龄限制",path:"ageLimit"},{default:n(()=>[s(t(D),{value:d.ageLimit,"onUpdate:value":a[3]||(a[3]=l=>d.ageLimit=l),options:N.value,placeholder:"请选择年龄限制",clearable:""},null,8,["value","options"])]),_:1}),s(t(B),{label:"会员门槛",path:"memberThreshold"},{default:n(()=>[s(t(D),{value:d.memberThreshold,"onUpdate:value":a[4]||(a[4]=l=>d.memberThreshold=l),options:I.value,placeholder:"请选择会员门槛",clearable:""},null,8,["value","options"])]),_:1}),s(t(B),{label:"活动时间",path:"activityTime"},{default:n(()=>[s(t(ve),{value:d.activityTime,"onUpdate:value":a[5]||(a[5]=l=>d.activityTime=l),type:"datetime",placeholder:"请选择活动时间",clearable:"",style:{width:"100%"}},null,8,["value"])]),_:1})]),_:1},8,["model"])],512),[[te,c.value===1]]),ee(i("div",at,[i("div",lt,[(x(!0),q(E,null,ue(v.value,l=>(x(),q("div",{key:l.id,class:"field-item"},[i("div",st,ce(l.label),1),i("div",it,[l.type==="text"?(x(),$(t(A),{key:0,placeholder:"请输入",disabled:""})):R("",!0),l.type==="richtext"?(x(),$(t(A),{key:1,type:"textarea",placeholder:"请输入",rows:3,disabled:""})):R("",!0),l.type==="select"?(x(),$(t(D),{key:2,placeholder:"请选择",disabled:""})):R("",!0),l.type==="date"?(x(),$(t(ve),{key:3,placeholder:"请选择日期",style:{width:"100%"},disabled:""})):R("",!0)]),i("div",ot,[l.isDefault?R("",!0):(x(),$(t(U),{key:0,text:"",type:"error",onClick:g=>P(l.id)},{default:n(()=>[...a[7]||(a[7]=[F(" 删除 ",-1)])]),_:1},8,["onClick"]))])]))),128))]),i("div",nt,[s(t(De),{trigger:"click",options:r,onSelect:m},{default:n(()=>[s(t(U),{text:"",type:"primary"},{icon:n(()=>[s(t(pe),{icon:"ri:add-line"})]),default:n(()=>[a[8]||(a[8]=F(" 新增字段 ",-1)),s(t(pe),{icon:"ri:arrow-down-s-line",style:{"margin-left":"4px"}})]),_:1})]),_:1})])],512),[[te,c.value===2]]),ee(i("div",rt,[i("div",ct,[a[10]||(a[10]=i("div",{class:"table-header"},[i("div",{class:"table-cell"},"优惠券类型"),i("div",{class:"table-cell"},"使用商户"),i("div",{class:"table-cell"},"使用时段"),i("div",{class:"table-cell"},"使用品类"),i("div",{class:"table-cell"},"定向发放"),i("div",{class:"table-cell"},"操作")],-1)),(x(!0),q(E,null,ue(T.value,l=>(x(),q("div",{key:l.id,class:"table-row"},[i("div",dt,[s(t(D),{value:l.type,"onUpdate:value":g=>l.type=g,options:V.value,placeholder:"请选择",size:"small"},null,8,["value","onUpdate:value","options"])]),i("div",ut,[s(t(D),{value:l.merchants,"onUpdate:value":g=>l.merchants=g,options:Q.value,placeholder:"请选择",multiple:"",size:"small"},null,8,["value","onUpdate:value","options"])]),i("div",pt,[s(t(A),{value:l.timeSlot,"onUpdate:value":g=>l.timeSlot=g,placeholder:"请输入时段",size:"small"},null,8,["value","onUpdate:value"])]),i("div",vt,[s(t(D),{value:l.category,"onUpdate:value":g=>l.category=g,options:H.value,placeholder:"请选择",size:"small"},null,8,["value","onUpdate:value","options"])]),i("div",mt,[s(t(je),{value:l.targetDistribution,"onUpdate:value":g=>l.targetDistribution=g},null,8,["value","onUpdate:value"])]),i("div",ht,[s(t(U),{text:"",type:"error",size:"small",onClick:g=>M(l.id)},{default:n(()=>[...a[9]||(a[9]=[F(" 删除 ",-1)])]),_:1},8,["onClick"])])]))),128))]),i("div",{class:"add-row-button"},[i("span",{class:"add-row-text",onClick:K},"+ 添加一行")])],512),[[te,c.value===3]]),i("div",bt,[s(t(Ae),{size:12},{default:n(()=>[c.value>1?(x(),$(t(U),{key:0,onClick:X},{default:n(()=>[...a[11]||(a[11]=[F(" 上一步 ",-1)])]),_:1})):R("",!0),c.value<3?(x(),$(t(U),{key:1,type:"primary",onClick:G},{default:n(()=>[...a[12]||(a[12]=[F(" 下一步 ",-1)])]),_:1})):R("",!0),c.value===3?(x(),$(t(U),{key:2,type:"primary",onClick:J},{default:n(()=>[...a[13]||(a[13]=[F(" 提交 ",-1)])]),_:1})):R("",!0)]),_:1})])])])]),_:1})]),_:1})]))}});const Ct=Be(ft,[["__scopeId","data-v-b63ed845"]]);export{Ct as default};

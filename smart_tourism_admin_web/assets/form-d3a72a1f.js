import{f as m,H as G,e as P,I as L,bI as J,G as he,d as ae,h as pe,L as be,k as ve,c4 as fe,K as ge,w as p,by as xe,bp as ye,bq as _e,c5 as ze,n as F,c6 as y,q as ke,F as le,c7 as se,bk as Y,bB as Se,bD as ie,c8 as we,c9 as Ce,bR as Ne,au as Ie,a2 as Te,r as x,bS as $e,o as g,c as B,b as s,ab as r,R as t,bU as Pe,a as i,ac as $,ca as Re,a6 as oe,A as Z,bo as ee,N as O,bX as re,aS as R,X as ne,aa as ce,Q as N,a1 as I,a5 as U,ar as Ue,ah as de,bW as De,b6 as Fe}from"./index-fc2ca07d.js";import{A as Be}from"./ArrowBack-24ac8c7f.js";import{g as qe}from"./Forward-86f34074.js";import{N as Le}from"./Form-97fa87e1.js";import{N as D}from"./FormItem-9918da75.js";import{N as ue}from"./DatePicker-f677266b.js";import{N as Oe}from"./Switch-3c24006e.js";import{N as je}from"./Space-29132ab6.js";const Ae=m("steps",`
 width: 100%;
 display: flex;
`,[m("step",`
 position: relative;
 display: flex;
 flex: 1;
 `,[G("disabled","cursor: not-allowed"),G("clickable",`
 cursor: pointer;
 `),P("&:last-child",[m("step-splitor","display: none;")])]),m("step-splitor",`
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
 `),m("step-content","flex: 1;",[m("step-content-header",`
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
 `,[L("title",`
 white-space: nowrap;
 flex: 0;
 `)]),L("description",`
 color: var(--n-description-text-color);
 margin-top: 12px;
 margin-left: 9px;
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `)]),m("step-indicator",`
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
 `,[m("step-indicator-slot",`
 position: relative;
 width: var(--n-indicator-icon-size);
 height: var(--n-indicator-icon-size);
 font-size: var(--n-indicator-icon-size);
 line-height: var(--n-indicator-icon-size);
 `,[L("index",`
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
 `,[J()]),m("icon",`
 color: var(--n-indicator-text-color);
 transition: color .3s var(--n-bezier);
 `,[J()]),m("base-icon",`
 color: var(--n-indicator-text-color);
 transition: color .3s var(--n-bezier);
 `,[J()])])]),G("vertical","flex-direction: column;",[he("show-description",[P(">",[m("step","padding-bottom: 8px;")])]),P(">",[m("step","margin-bottom: 16px;",[P("&:last-child","margin-bottom: 0;"),P(">",[m("step-indicator",[P(">",[m("step-splitor",`
 position: absolute;
 bottom: -8px;
 width: 1px;
 margin: 0 !important;
 left: calc(var(--n-indicator-size) / 2);
 height: calc(100% - var(--n-indicator-size));
 `)])]),m("step-content",[L("description","margin-top: 8px;")])])])])])]);function Ee(e,v){return typeof e!="object"||e===null||Array.isArray(e)?null:(e.props||(e.props={}),e.props.internalIndex=v+1,e)}function Ve(e){return e.map((v,h)=>Ee(v,h))}const Qe=Object.assign(Object.assign({},ve.props),{current:Number,status:{type:String,default:"process"},size:{type:String,default:"medium"},vertical:Boolean,"onUpdate:current":[Function,Array],onUpdateCurrent:[Function,Array]}),me=ye("n-steps"),He=ae({name:"Steps",props:Qe,slots:Object,setup(e,{slots:v}){const{mergedClsPrefixRef:h,mergedRtlRef:d}=pe(e),z=be("Steps",d,h),_=ve("Steps","-steps",Ae,fe,e,h);return ge(me,{props:e,mergedThemeRef:_,mergedClsPrefixRef:h,stepsSlots:v}),{mergedClsPrefix:h,rtlEnabled:z}},render(){const{mergedClsPrefix:e}=this;return p("div",{class:[`${e}-steps`,this.rtlEnabled&&`${e}-steps--rtl`,this.vertical&&`${e}-steps--vertical`]},Ve(xe(qe(this))))}}),Ke={status:String,title:String,description:String,disabled:Boolean,internalIndex:{type:Number,default:0}},te=ae({name:"Step",props:Ke,slots:Object,setup(e){const v=_e(me,null);v||ze("step","`n-step` must be placed inside `n-steps`.");const{inlineThemeDisabled:h}=pe(),{props:d,mergedThemeRef:z,mergedClsPrefixRef:_,stepsSlots:o}=v,T=F(()=>d.vertical),n=F(()=>{const{status:c}=e;if(c)return c;{const{internalIndex:u}=e,{current:w}=d;if(w===void 0)return"process";if(u<w)return"finish";if(u===w)return d.status||"process";if(u>w)return"wait"}return"process"}),q=F(()=>{const{value:c}=n,{size:u}=d,{common:{cubicBezierEaseInOut:w},self:{stepHeaderFontWeight:j,[y("stepHeaderFontSize",u)]:C,[y("indicatorIndexFontSize",u)]:A,[y("indicatorSize",u)]:E,[y("indicatorIconSize",u)]:V,[y("indicatorTextColor",c)]:Q,[y("indicatorBorderColor",c)]:H,[y("headerTextColor",c)]:K,[y("splitorColor",c)]:M,[y("indicatorColor",c)]:W,[y("descriptionTextColor",c)]:X}}=z.value;return{"--n-bezier":w,"--n-description-text-color":X,"--n-header-text-color":K,"--n-indicator-border-color":H,"--n-indicator-color":W,"--n-indicator-icon-size":V,"--n-indicator-index-font-size":A,"--n-indicator-size":E,"--n-indicator-text-color":Q,"--n-splitor-color":M,"--n-step-header-font-size":C,"--n-step-header-font-weight":j}}),k=h?ke("step",F(()=>{const{value:c}=n,{size:u}=d;return`${c[0]}${u[0]}`}),q,d):void 0,S=F(()=>{if(e.disabled)return;const{onUpdateCurrent:c,"onUpdate:current":u}=d;return c||u?()=>{c&&le(c,e.internalIndex),u&&le(u,e.internalIndex)}:void 0});return{stepsSlots:o,mergedClsPrefix:_,vertical:T,mergedStatus:n,handleStepClick:S,cssVars:h?void 0:q,themeClass:k==null?void 0:k.themeClass,onRender:k==null?void 0:k.onRender}},render(){const{mergedClsPrefix:e,onRender:v,handleStepClick:h,disabled:d}=this,z=se(this.$slots.default,_=>{const o=_||this.description;return o?p("div",{class:`${e}-step-content__description`},o):null});return v==null||v(),p("div",{class:[`${e}-step`,d&&`${e}-step--disabled`,!d&&h&&`${e}-step--clickable`,this.themeClass,z&&`${e}-step--show-description`,`${e}-step--${this.mergedStatus}-status`],style:this.cssVars,onClick:h},p("div",{class:`${e}-step-indicator`},p("div",{class:`${e}-step-indicator-slot`},p(Se,null,{default:()=>se(this.$slots.icon,_=>{const{mergedStatus:o,stepsSlots:T}=this;return o==="finish"||o==="error"?o==="finish"?p(ie,{clsPrefix:e,key:"finish"},{default:()=>Y(T["finish-icon"],()=>[p(we,null)])}):o==="error"?p(ie,{clsPrefix:e,key:"error"},{default:()=>Y(T["error-icon"],()=>[p(Ce,null)])}):null:_||p("div",{key:this.internalIndex,class:`${e}-step-indicator-slot__index`},this.internalIndex)})})),this.vertical?p("div",{class:`${e}-step-splitor`}):null),p("div",{class:`${e}-step-content`},p("div",{class:`${e}-step-content-header`},p("div",{class:`${e}-step-content-header__title`},Y(this.$slots.title,()=>[this.title])),this.vertical?null:p("div",{class:`${e}-step-splitor`})),z))}}),Me={class:"activity-form-container"},We={class:"header-section"},Xe={class:"header-left"},Ge={class:"header-title"},Je={class:"steps-section"},Ye={class:"content-section"},Ze={class:"content-wrapper"},et={class:"step-content"},tt={class:"step-content"},at={class:"template-fields"},lt={class:"field-label"},st={class:"field-type"},it={class:"field-actions"},ot={class:"add-field-button"},rt={class:"step-content"},nt={class:"coupon-table"},ct={class:"table-cell"},dt={class:"table-cell"},ut={class:"table-cell"},pt={class:"table-cell"},vt={class:"table-cell"},mt={class:"table-cell"},ht={class:"footer-actions"},bt=ae({__name:"form",setup(e){const v=Ne(),h=Ie(),d=Te(),z=x(!!h.query.id),_=x(z.value?"编辑活动":"新增活动"),o=x(1),T=x(null),n=$e({activityName:"",totalQuota:null,maxPerPerson:null,ageLimit:null,memberThreshold:null,activityTime:null}),q=x([{label:"不限",value:"unlimited"},{label:"3-12岁",value:"3-12"},{label:"12-18岁",value:"12-18"},{label:"18-30岁",value:"18-30"},{label:"18-60岁",value:"18-60"},{label:"30-50岁",value:"30-50"}]),k=x([{label:"无限制",value:"unlimited"},{label:"等级1",value:"level1"},{label:"等级2",value:"level2"},{label:"等级3",value:"level3"},{label:"等级4",value:"level4"},{label:"等级5",value:"level5"}]),S=x([{id:1,label:"姓名",type:"text",required:!0,isDefault:!0},{id:2,label:"手机号",type:"text",required:!0,isDefault:!0},{id:3,label:"账号名称",type:"text",required:!0,isDefault:!0},{id:4,label:"备注",type:"richtext",required:!1,isDefault:!0}]),c=b=>{const a=S.value.length>0?Math.max(...S.value.map(f=>f.id))+1:1,l={text:"单文本",richtext:"富文本",select:"选择框",date:"日期框"};S.value.push({id:a,label:`${l[b]}字段${a}`,type:b,required:!1,isDefault:!1}),d.success("字段添加成功")},u=[{label:"单文本",key:"text"},{label:"富文本",key:"richtext"},{label:"选择框",key:"select"},{label:"日期框",key:"date"}],w=b=>{c(b)},j=b=>{S.value=S.value.filter(a=>a.id!==b),d.success("字段删除成功")},C=x([]),A=x([{label:"满减券",value:"cash"},{label:"折扣券",value:"discount"}]),E=x([{label:"不限制",value:"unlimited"},{label:"美味餐厅",value:"merchant1"},{label:"舒适酒店",value:"merchant2"},{label:"欢乐KTV",value:"merchant3"},{label:"时尚购物中心",value:"merchant4"},{label:"咖啡时光",value:"merchant5"}]),V=x([{label:"餐饮类",value:"catering"},{label:"购物类",value:"shopping"},{label:"娱乐类",value:"entertainment"},{label:"住宿类",value:"accommodation"}]),Q=()=>{const b=C.value.length>0?Math.max(...C.value.map(a=>a.id))+1:1;C.value.push({id:b,type:"",merchants:[],timeSlot:"",category:"",targetDistribution:!1})},H=b=>{C.value=C.value.filter(a=>a.id!==b)},K=()=>{v.back()},M=()=>{o.value>1&&o.value--},W=()=>{var b;o.value===1?(b=T.value)==null||b.validate(a=>{a||(o.value=2)}):o.value===2&&(o.value=3)},X=()=>{d.success("活动保存成功"),setTimeout(()=>{v.push("/activity")},1e3)};return(b,a)=>(g(),B("div",Me,[s(t(De),{"has-sider":"",class:"h-full w-full"},{default:r(()=>[s(t(Pe),{class:"h-full flex flex-col"},{default:r(()=>[i("div",We,[i("div",Xe,[s(t($),{text:"",onClick:K,class:"back-button"},{icon:r(()=>[s(t(Re),{size:"20"},{default:r(()=>[s(t(Be))]),_:1})]),_:1}),i("span",Ge,oe(_.value),1)]),a[6]||(a[6]=i("div",{class:"header-placeholder"},null,-1))]),i("div",Je,[s(t(He),{current:o.value,class:"steps-container"},{default:r(()=>[s(t(te),{title:"活动信息"}),s(t(te),{title:"报名模板配置"}),s(t(te),{title:"优惠券配置"})]),_:1},8,["current"])]),i("div",Ye,[i("div",Ze,[Z(i("div",et,[s(t(Le),{ref_key:"activityFormRef",ref:T,model:n,rules:{activityName:{required:!0,message:"请输入活动名称",trigger:"blur"},totalQuota:{required:!0,message:"请输入总名额限制",trigger:"blur",type:"number"},maxPerPerson:{required:!0,message:"请输入单人最大报名数",trigger:"blur",type:"number"},ageLimit:{required:!0,message:"请选择年龄限制",trigger:"change"},memberThreshold:{required:!0,message:"请选择会员门槛",trigger:"change"},activityTime:{required:!0,message:"请选择活动时间",trigger:"change",type:"number"}},"label-placement":"left","label-width":"140px"},{default:r(()=>[s(t(D),{label:"活动名称",path:"activityName"},{default:r(()=>[s(t(O),{value:n.activityName,"onUpdate:value":a[0]||(a[0]=l=>n.activityName=l),placeholder:"请输入活动名称",clearable:""},null,8,["value"])]),_:1}),s(t(D),{label:"总名额限制",path:"totalQuota"},{default:r(()=>[s(t(re),{value:n.totalQuota,"onUpdate:value":a[1]||(a[1]=l=>n.totalQuota=l),placeholder:"请输入总名额限制",min:1,style:{width:"100%"}},null,8,["value"])]),_:1}),s(t(D),{label:"单人最大报名数",path:"maxPerPerson"},{default:r(()=>[s(t(re),{value:n.maxPerPerson,"onUpdate:value":a[2]||(a[2]=l=>n.maxPerPerson=l),placeholder:"请输入单人最大报名数",min:1,style:{width:"100%"}},null,8,["value"])]),_:1}),s(t(D),{label:"年龄限制",path:"ageLimit"},{default:r(()=>[s(t(R),{value:n.ageLimit,"onUpdate:value":a[3]||(a[3]=l=>n.ageLimit=l),options:q.value,placeholder:"请选择年龄限制",clearable:""},null,8,["value","options"])]),_:1}),s(t(D),{label:"会员门槛",path:"memberThreshold"},{default:r(()=>[s(t(R),{value:n.memberThreshold,"onUpdate:value":a[4]||(a[4]=l=>n.memberThreshold=l),options:k.value,placeholder:"请选择会员门槛",clearable:""},null,8,["value","options"])]),_:1}),s(t(D),{label:"活动时间",path:"activityTime"},{default:r(()=>[s(t(ue),{value:n.activityTime,"onUpdate:value":a[5]||(a[5]=l=>n.activityTime=l),type:"datetime",placeholder:"请选择活动时间",clearable:"",style:{width:"100%"}},null,8,["value"])]),_:1})]),_:1},8,["model"])],512),[[ee,o.value===1]]),Z(i("div",tt,[i("div",at,[(g(!0),B(ne,null,ce(S.value,l=>(g(),B("div",{key:l.id,class:"field-item"},[i("div",lt,oe(l.label),1),i("div",st,[l.type==="text"?(g(),N(t(O),{key:0,placeholder:"请输入",disabled:""})):I("",!0),l.type==="richtext"?(g(),N(t(O),{key:1,type:"textarea",placeholder:"请输入",rows:3,disabled:""})):I("",!0),l.type==="select"?(g(),N(t(R),{key:2,placeholder:"请选择",disabled:""})):I("",!0),l.type==="date"?(g(),N(t(ue),{key:3,placeholder:"请选择日期",style:{width:"100%"},disabled:""})):I("",!0)]),i("div",it,[l.isDefault?I("",!0):(g(),N(t($),{key:0,text:"",type:"error",onClick:f=>j(l.id)},{default:r(()=>a[7]||(a[7]=[U(" 删除 ")])),_:2},1032,["onClick"]))])]))),128))]),i("div",ot,[s(t(Ue),{trigger:"click",options:u,onSelect:w},{default:r(()=>[s(t($),{text:"",type:"primary"},{icon:r(()=>[s(t(de),{icon:"ri:add-line"})]),default:r(()=>[a[8]||(a[8]=U(" 新增字段 ")),s(t(de),{icon:"ri:arrow-down-s-line",style:{"margin-left":"4px"}})]),_:1})]),_:1})])],512),[[ee,o.value===2]]),Z(i("div",rt,[i("div",nt,[a[10]||(a[10]=i("div",{class:"table-header"},[i("div",{class:"table-cell"},"优惠券类型"),i("div",{class:"table-cell"},"使用商户"),i("div",{class:"table-cell"},"使用时段"),i("div",{class:"table-cell"},"使用品类"),i("div",{class:"table-cell"},"定向发放"),i("div",{class:"table-cell"},"操作")],-1)),(g(!0),B(ne,null,ce(C.value,l=>(g(),B("div",{key:l.id,class:"table-row"},[i("div",ct,[s(t(R),{value:l.type,"onUpdate:value":f=>l.type=f,options:A.value,placeholder:"请选择",size:"small"},null,8,["value","onUpdate:value","options"])]),i("div",dt,[s(t(R),{value:l.merchants,"onUpdate:value":f=>l.merchants=f,options:E.value,placeholder:"请选择",multiple:"",size:"small"},null,8,["value","onUpdate:value","options"])]),i("div",ut,[s(t(O),{value:l.timeSlot,"onUpdate:value":f=>l.timeSlot=f,placeholder:"请输入时段",size:"small"},null,8,["value","onUpdate:value"])]),i("div",pt,[s(t(R),{value:l.category,"onUpdate:value":f=>l.category=f,options:V.value,placeholder:"请选择",size:"small"},null,8,["value","onUpdate:value","options"])]),i("div",vt,[s(t(Oe),{value:l.targetDistribution,"onUpdate:value":f=>l.targetDistribution=f},null,8,["value","onUpdate:value"])]),i("div",mt,[s(t($),{text:"",type:"error",size:"small",onClick:f=>H(l.id)},{default:r(()=>a[9]||(a[9]=[U(" 删除 ")])),_:2},1032,["onClick"])])]))),128))]),i("div",{class:"add-row-button"},[i("span",{class:"add-row-text",onClick:Q},"+ 添加一行")])],512),[[ee,o.value===3]]),i("div",ht,[s(t(je),{size:12},{default:r(()=>[o.value>1?(g(),N(t($),{key:0,onClick:M},{default:r(()=>a[11]||(a[11]=[U(" 上一步 ")])),_:1})):I("",!0),o.value<3?(g(),N(t($),{key:1,type:"primary",onClick:W},{default:r(()=>a[12]||(a[12]=[U(" 下一步 ")])),_:1})):I("",!0),o.value===3?(g(),N(t($),{key:2,type:"primary",onClick:X},{default:r(()=>a[13]||(a[13]=[U(" 提交 ")])),_:1})):I("",!0)]),_:1})])])])]),_:1})]),_:1})]))}});const wt=Fe(bt,[["__scopeId","data-v-82bb3060"]]);export{wt as default};

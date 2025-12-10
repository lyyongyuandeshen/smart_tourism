from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SSOAuthRequest(BaseModel):
    """SSO授权请求模型"""
    app_client_id: str = Field(..., description="客户端标识")
    callback_url: str = Field(..., description="回调地址")


class AccessTokenRequest(BaseModel):
    """获取访问令牌请求模型"""
    code: str = Field(..., description="授权码")


class UserInfoRequest(BaseModel):
    """获取用户信息请求模型"""
    code: str = Field(..., description="授权码")
    access_token: str = Field(..., description="访问令牌")


class SSOLoginRequest(BaseModel):
    """SSO一键登录请求模型"""
    code: str = Field(..., description="授权码")


class UserDept(BaseModel):
    """用户部门信息"""
    leader_status: int = Field(..., alias="leaderStatus", description="领导状态")
    dept_name: str = Field(..., alias="deptName", description="部门名称")
    dept_id: str = Field(..., alias="deptId", description="部门ID")
    main_dept: str = Field(..., alias="mainDept", description="主部门")
    sort_num: int = Field(..., alias="sortNum", description="排序号")
    dept_code: str = Field(..., alias="deptCode", description="部门编码")


class UserInfo(BaseModel):
    """用户信息模型"""
    user_industry_id: str = Field(..., alias="userIndustryId", description="用户行业ID")
    business_license: str = Field(..., alias="businessLicense", description="营业执照")
    user_status: int = Field(..., alias="userStatus", description="用户状态")
    user_real_name: str = Field(..., alias="userRealName", description="用户真实姓名")
    del_flag: int = Field(..., alias="delFlag", description="删除标志")
    credit_type: str = Field(..., alias="creditType", description="证件类型")
    custom_tag_ids: List[str] = Field(default=[], alias="customTagIds", description="自定义标签ID")
    use_situation: str = Field(..., alias="useSituation", description="使用情况")
    credit_id: str = Field(..., alias="creditId", description="身份证号")
    custom_tags: List[str] = Field(default=[], alias="customTags", description="自定义标签")
    user_mobile: str = Field(..., alias="userMobile", description="用户手机号")
    id: str = Field(..., description="用户ID")
    enterprise_name: str = Field(..., alias="enterpriseName", description="企业名称")
    is_three_in_one: str = Field(..., alias="isThreeInOne", description="是否三证合一")
    political_status: str = Field(..., alias="politicalStatus", description="政治面貌")
    user_remarks: str = Field(..., alias="userRemarks", description="用户备注")
    update_time: str = Field(..., alias="updateTime", description="更新时间")
    user_name: str = Field(..., alias="userName", description="用户名")
    custom_tag_names: List[str] = Field(default=[], alias="customTagNames", description="自定义标签名称")
    user_depts: List[UserDept] = Field(default=[], alias="userDepts", description="用户部门")
    user_gender: int = Field(..., alias="userGender", description="用户性别")
    user_type: str = Field(..., alias="userType", description="用户类型")
    enterprise_id: str = Field(..., alias="enterpriseId", description="企业ID")
    preparation_type: str = Field(..., alias="preparationType", description="筹备类型")
    user_biz_email: str = Field(..., alias="userBizEmail", description="用户业务邮箱")


class AccessTokenResponse(BaseModel):
    """访问令牌响应模型"""
    code: int = Field(..., description="状态码")
    msg: str = Field(..., description="响应信息")
    data: Dict[str, Any] = Field(..., description="响应数据")


class UserInfoResponse(BaseModel):
    """用户信息响应模型"""
    code: int = Field(..., description="状态码")
    msg: str = Field(..., description="响应信息")
    data: Dict[str, Any] = Field(..., description="响应数据")


class SSOLoginResponse(BaseModel):
    """SSO登录响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[Dict[str, Any]] = Field(None, description="用户数据")
    access_token: Optional[str] = Field(None, description="访问令牌")
    user_info: Optional[UserInfo] = Field(None, description="用户信息")


class SSOErrorResponse(BaseModel):
    """SSO错误响应模型"""
    success: bool = Field(False, description="是否成功")
    message: str = Field(..., description="错误消息")
    error_code: Optional[str] = Field(None, description="错误代码")
    detail: Optional[str] = Field(None, description="错误详情")
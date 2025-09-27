# RESTful API 重构契约文档 (RESTful API Refactoring Contracts)

**项目名称**: [项目名称]  
**重构目标**: [重构目标]  
**源系统路径**: [源代码路径]  
**提取日期**: [日期]  
**分析范围**: [后端REST API重构]

---

## 1. 现有API端点分析 (Current API Endpoint Analysis)

### 1.1 API端点映射

#### API Group: [APIGroupName]
**业务领域**: [业务领域描述]  
**API版本**: [v1/v2/etc]  
**重构影响**: [关键/一般/无影响]

**端点列表**:
| 方法 | 端点路径 | 描述 | 认证要求 | 重构约束 |
|------|----------|------|----------|----------|
| GET | `/api/[resource]` | [功能描述] | [Required/Optional] | [保持/优化] |
| POST | `/api/[resource]` | [功能描述] | [Required/Optional] | [保持/优化] |
| PUT | `/api/[resource]/{id}` | [功能描述] | [Required/Optional] | [保持/优化] |
| DELETE | `/api/[resource]/{id}` | [功能描述] | [Required/Optional] | [保持/优化] |

**详细端点定义**:
```typescript
// GET /api/[resource]
interface Get[Resource]Request {
  [param_name]: [type];  // [参数说明]
  [param_name]: [type];  // [参数说明]
}

interface Get[Resource]Response {
  success: boolean;
  data: [ResourceDTO][] | [ResourceDTO];
  message: string;
  timestamp: string;
}
```

### 1.2 API参数规范

#### 路径参数
| 参数名 | 类型 | 必需 | 描述 | 验证规则 |
|--------|------|------|------|----------|
| [param] | [type] | [yes/no] | [描述] | [验证规则] |

#### 查询参数
| 参数名 | 类型 | 默认值 | 描述 | 验证规则 |
|--------|------|--------|------|----------|
| [param] | [type] | [default] | [描述] | [验证规则] |

#### 请求体
```typescript
interface Create[Resource]Request {
  [field_name]: [type];  // [字段说明 + 验证规则]
  [field_name]: [type];  // [字段说明 + 验证规则]
}
```

---

## 2. 数据模型契约 (Data Model Contracts)

### 2.1 实体数据传输对象 (DTOs)

#### DTO: [ResourceDTO]
**对应实体**: [EntityName]  
**使用场景**: [使用场景描述]

**DTO定义**:
```typescript
interface [ResourceDTO] {
  id: string;                    // 唯一标识符
  [field_name]: [field_type];     // [字段说明]
  [field_name]: [field_type];     // [字段说明]
  createdDate: Date;              // 创建时间
  updatedDate: Date;              // 更新时间
  // ... 其他字段
}
```

**字段约束**:
| 字段名 | 类型 | 必需 | 默认值 | 约束条件 |
|--------|------|------|--------|----------|
| [field] | [type] | [yes/no] | [default] | [constraint] |

### 2.2 复杂DTO结构

#### 嵌套DTO: [NestedDTO]
**父DTO**: [ParentDTO]  
**嵌套关系**: [关系描述]

**嵌套结构**:
```typescript
interface [NestedDTO] {
  [nested_field]: [NestedType];  // 嵌套对象
  [array_field]: [ArrayType][];  // 嵌套数组
  // ... 其他字段
}
```

#### 联合DTO: [JunctionDTO]
**关联实体**: [Entity1] + [Entity2]  
**业务意义**: [业务说明]

**联合结构**:
```typescript
interface [JunctionDTO] {
  [entity1]: [Entity1DTO];      // 实体1数据
  [entity2]: [Entity2DTO];      // 实体2数据
  [junction_field]: [type];     // 联合字段
}
```

---

## 3. API响应契约 (API Response Contracts)

### 3.1 标准响应格式

#### 成功响应
```typescript
interface StandardSuccessResponse<T> {
  success: true;
  data: T;                       // 响应数据
  message: string;               // 成功消息
  timestamp: string;             // 响应时间戳
  requestId?: string;            // 请求ID（可选）
}
```

#### 错误响应
```typescript
interface StandardErrorResponse {
  success: false;
  error: {
    code: string;                // 错误代码
    message: string;             // 错误消息
    details?: any;               // 错误详情（可选）
    stack?: string;              // 错误堆栈（开发环境）
  };
  timestamp: string;             // 响应时间戳
  requestId?: string;            // 请求ID（可选）
}
```

### 3.2 分页响应

#### 分页格式
```typescript
interface PaginatedResponse<T> {
  success: true;
  data: {
    items: T[];                 // 数据项列表
    pagination: {
      page: number;              // 当前页码
      pageSize: number;          // 每页大小
      total: number;             // 总记录数
      totalPages: number;        // 总页数
      hasNext: boolean;          // 是否有下一页
      hasPrev: boolean;          // 是否有上一页
    };
  };
  message: string;
  timestamp: string;
}
```

### 3.3 批量操作响应

#### 批量创建/更新
```typescript
interface BatchOperationResponse {
  success: true;
  data: {
    successful: number;          // 成功数量
    failed: number;              // 失败数量
    results: BatchResult[];      // 详细结果
  };
  message: string;
  timestamp: string;
}

interface BatchResult {
  item: any;                     // 操作项
  success: boolean;              // 是否成功
  error?: string;                // 错误信息（失败时）
  id?: string;                   // 生成ID（成功时）
}
```

---

## 4. 认证与授权契约 (Authentication & Authorization Contracts)

### 4.1 认证机制

#### JWT令牌认证
```typescript
interface JWTPayload {
  sub: string;                   // 用户ID
  username: string;             // 用户名
  email: string;                 // 邮箱
  roles: string[];               // 用户角色
  permissions: string[];         // 用户权限
  exp: number;                   // 过期时间
  iat: number;                   // 签发时间
}
```

#### API密钥认证
```typescript
interface APIKey {
  key: string;                   // API密钥
  secret: string;                // API密钥
  permissions: string[];         // 权限范围
  rateLimit: number;            // 速率限制
}
```

### 4.2 权限控制

#### 端点权限要求
| 端点 | 所需角色 | 所需权限 | 访问级别 |
|------|----------|----------|----------|
| GET /api/[resource] | [role1,role2] | [permission1,permission2] | [public/authenticated/admin] |
| POST /api/[resource] | [role1] | [permission1] | [authenticated] |
| PUT /api/[resource]/{id} | [role1,role2] | [permission1,permission2] | [authenticated] |

#### 权限验证逻辑
```typescript
// 权限检查中间件
const checkPermission = (requiredPermissions: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const userPermissions = req.user?.permissions || [];
    const hasPermission = requiredPermissions.every(perm => 
      userPermissions.includes(perm)
    );
    
    if (!hasPermission) {
      return res.status(403).json({
        success: false,
        error: {
          code: 'INSUFFICIENT_PERMISSIONS',
          message: 'Insufficient permissions to access this resource'
        }
      });
    }
    
    next();
  };
};
```

---

## 5. 错误处理契约 (Error Handling Contracts)

### 5.1 标准错误代码

#### HTTP状态码映射
| HTTP状态 | 错误代码 | 错误类型 | 描述 |
|----------|----------|----------|------|
| 400 | BAD_REQUEST | 客户端错误 | 请求参数错误 |
| 401 | UNAUTHORIZED | 认证失败 | 未认证或认证失败 |
| 403 | FORBIDDEN | 权限不足 | 无权限访问资源 |
| 404 | NOT_FOUND | 资源不存在 | 请求的资源不存在 |
| 409 | CONFLICT | 资源冲突 | 资源状态冲突 |
| 422 | VALIDATION_ERROR | 验证失败 | 数据验证失败 |
| 429 | RATE_LIMITED | 限流 | 请求频率超限 |
| 500 | INTERNAL_ERROR | 服务器错误 | 服务器内部错误 |

#### 业务错误代码
| 错误代码 | HTTP状态 | 描述 | 触发条件 |
|----------|----------|------|----------|
| [ERROR_CODE] | [status] | [description] | [condition] |
| [ERROR_CODE] | [status] | [description] | [condition] |

### 5.2 错误响应格式

#### 验证错误
```typescript
interface ValidationErrorResponse {
  success: false;
  error: {
    code: 'VALIDATION_ERROR';
    message: 'Request validation failed';
    details: {
      field: string;              // 错误字段
      message: string;            // 错误消息
      value?: any;                // 错误值
      constraints?: string[];     // 约束条件
    }[];
  };
  timestamp: string;
}
```

#### 业务逻辑错误
```typescript
interface BusinessErrorResponse {
  success: false;
  error: {
    code: string;                // 业务错误代码
    message: string;             // 错误消息
    details?: {
      businessRule: string;      // 违反的业务规则
      expected: any;             // 期望值
      actual: any;               // 实际值
    };
  };
  timestamp: string;
}
```

---

## 6. 性能与限流契约 (Performance & Rate Limiting Contracts)

### 6.1 API限流策略

#### 限流配置
| API端点 | 速率限制 | 突发限制 | 时间窗口 | 优先级 |
|----------|----------|----------|----------|--------|
| GET /api/[resource] | 100/分钟 | 10/秒 | 1分钟 | 高 |
| POST /api/[resource] | 20/分钟 | 5/秒 | 1分钟 | 中 |
| PUT /api/[resource]/{id} | 50/分钟 | 5/秒 | 1分钟 | 中 |

#### 限流响应
```typescript
interface RateLimitResponse {
  success: false;
  error: {
    code: 'RATE_LIMITED';
    message: 'Rate limit exceeded';
    details: {
      limit: number;              // 限制数量
      remaining: number;          // 剩余数量
      reset: string;              // 重置时间
      retryAfter: number;         // 重试间隔（秒）
    };
  };
  timestamp: string;
}
```

### 6.2 缓存策略

#### 缓存配置
| 数据类型 | 缓存时间 | 缓存键 | 缓存策略 |
|----------|----------|--------|----------|
| [Resource]数据 | 5分钟 | [cache_key] | [TTL/LRU] |
| 用户信息 | 10分钟 | [cache_key] | [TTL/LRU] |
| 配置数据 | 1小时 | [cache_key] | [TTL/LRU] |

#### 缓存头设置
```typescript
// Cache-Control头设置
const getCacheHeaders = (maxAge: number) => ({
  'Cache-Control': `public, max-age=${maxAge}`,
  'ETag': generateETag(data),
  'Last-Modified': new Date().toUTCString()
});
```

---

## 7. 重构约束条件 (Refactoring Constraints)

### 7.1 不可变更的契约

#### 接口稳定性 - Constitution II (NON-NEGOTIABLE)
- [ ] **端点路径**: 所有HTTP端点路径必须100%保持
- [ ] **HTTP方法**: 请求方法必须完全一致
- [ ] **参数结构**: 请求参数名称、类型、结构必须保持
- [ ] **响应格式**: 响应数据结构、字段名称、类型必须保持
- [ ] **错误处理**: 错误码、错误消息、HTTP状态码必须保持一致

#### 数据契约完整性 - Constitution III + VI-D
- [ ] **DTO结构**: 数据传输对象的属性、类型、约束必须保持
- [ ] **验证规则**: 数据验证逻辑和错误提示必须保持
- [ ] **关联关系**: 实体间的关系和约束必须保持
- [ ] **默认值**: 字段默认值和初始化逻辑必须保持

#### 业务逻辑保持 - Constitution I (NON-NEGOTIABLE)
- [ ] **业务规则**: 核心业务规则的计算逻辑必须保持
- [ ] **权限控制**: 权限检查和控制逻辑必须保持
- [ ] **事务处理**: 事务边界和回滚逻辑必须保持
- [ ] **数据一致性**: 数据一致性检查机制必须保持

#### 数据真实性 - Constitution VI-C (NON-NEGOTIABLE)
- [ ] **真实数据源**: API必须连接真实的数据库
- [ ] **生产环境**: 必须使用生产级别的数据源
- [ ] **数据验证**: 必须验证所有数据的真实性和来源可靠性

### 7.2 允许优化的范围

#### 实现层面
- [x] **代码结构**: 可以优化代码组织和模块划分
- [x] **算法优化**: 可以优化算法性能（不改变结果）
- [x] **数据库优化**: 可以优化查询性能和索引
- [x] **并发处理**: 可以优化并发和异步处理

#### 非功能性
- [x] **性能优化**: 提升响应速度和吞吐量
- [x] **可扩展性**: 增强系统的可扩展能力
- [x] **可维护性**: 改善代码的可读性和可维护性
- [x] **监控能力**: 增强监控和可观测性

---

## 8. 验证策略 (Verification Strategy)

### 8.1 API兼容性验证

#### 接口对比测试
```bash
#!/bin/bash
# API兼容性验证脚本
# 1. 端点对比验证
compare_api_endpoints old_system new_system

# 2. 请求响应格式验证
validate_request_response_format old_api new_api

# 3. 错误处理一致性验证
validate_error_handling old_system new_system

# 4. 性能基准测试
run_performance_benchmark old_system new_system
```

#### 自动化测试
```typescript
// API兼容性测试套件
describe('API Compatibility Tests', () => {
  it('should maintain endpoint structure', async () => {
    const oldEndpoints = await getOldSystemEndpoints();
    const newEndpoints = await getNewSystemEndpoints();
    
    expect(newEndpoints).toEqual(oldEndpoints);
  });
  
  it('should maintain response format', async () => {
    const response = await axios.get('/api/resource');
    expect(response.data).toMatchSchema(expectedSchema);
  });
});
```

### 8.2 性能基准验证

| 性能指标 | 原系统基准 | 目标要求 | 测试方法 | 验证频率 |
|----------|------------|----------|----------|----------|
| 响应时间 | [baseline]ms | ≤[target]ms | 压力测试 | 每次发布 |
| 并发用户 | [baseline] | ≥[target] | 负载测试 | 每次发布 |
| 错误率 | [baseline]% | ≤[target]% | 稳定性测试 | 每次发布 |
| 吞吐量 | [baseline]req/s | ≥[target]req/s | 性能测试 | 每次发布 |

### 8.3 数据一致性验证

#### 数据对比测试
```typescript
// 数据一致性验证
describe('Data Consistency Tests', () => {
  it('should return consistent data structure', async () => {
    const oldResponse = await oldSystem.getData();
    const newResponse = await newSystem.getData();
    
    expect(newResponse.data).toEqual(oldResponse.data);
  });
  
  it('should maintain data relationships', async () => {
    const relationships = await newSystem.getRelationships();
    expect(relationships).toMatchRelationshipSchema();
  });
});
```

---

## 9. 风险控制与回滚策略 (Risk Control & Rollback)

### 9.1 高风险变更识别

| 变更类别 | 风险描述 | 影响范围 | 风险等级 | 缓解措施 |
|----------|----------|----------|----------|----------|
| API端点变更 | 端点路径或方法变更 | 所有客户端应用 | [高/中/低] | [缓解方案] |
| 数据结构变更 | DTO结构变更 | 数据传输和解析 | [高/中/低] | [缓解方案] |
| 业务逻辑变更 | 业务规则变更 | 业务流程 | [高/中/低] | [缓解方案] |

### 9.2 渐进式发布策略

#### 阶段1: 影子测试
- **目标**: 验证新API的正确性
- **策略**: 新API与旧API并行运行，对比结果
- **退出条件**: 连续[X]小时无差异
- **回滚方案**: 停止新API，保持旧API

#### 阶段2: 流量切换
- **目标**: 逐步将流量切换到新API
- **策略**: [1% → 10% → 50% → 100%]
- **监控指标**: 错误率、响应时间、业务指标
- **回滚方案**: 立即切换回旧API

#### 阶段3: 稳定运行
- **目标**: 确保新API稳定运行
- **策略**: 全流量运行[X]天
- **监控**: 24/7监控和告警
- **回滚方案**: 紧急回滚到旧API

### 9.3 回滚执行计划

#### 回滚触发条件
- [ ] 错误率超过 [阈值] 持续 [时间]
- [ ] 响应时间超过 [阈值] 持续 [时间]
- [ ] 业务指标异常（如订单量下降 [百分比]%）
- [ ] 数据不一致或丢失
- [ ] 第三方依赖异常

#### 回滚步骤
```bash
#!/bin/bash
# API回滚脚本
# 1. 停止新API服务
stop_new_api_service

# 2. 启动旧API服务
start_old_api_service

# 3. 数据库回滚（如果需要）
rollback_database_changes

# 4. 负载均衡配置
update_load_balancer old_api

# 5. 验证系统状态
verify_api_health

# 6. 通知相关人员
notify_stakeholders "API已回滚"
```

---

## 10. 合规检查清单 (Compliance Checklist)

### 10.1 重构前检查
- [ ] 所有API契约已完整提取和文档化
- [ ] 所有业务规则已识别和验证
- [ ] 数据模型映射已完成
- [ ] 风险评估已完成
- [ ] 回滚方案已准备就绪
- [ ] 测试用例已准备完成

### 10.2 重构中检查
- [ ] API接口实现与契约100%一致
- [ ] 业务逻辑保持完全一致
- [ ] 数据验证规则保持不变
- [ ] 错误处理机制保持一致
- [ ] 性能指标满足要求
- [ ] 安全控制措施保持有效

### 10.3 重构后验证
- [ ] 所有测试用例通过
- [ ] 性能指标达到基准要求
- [ ] 业务指标正常
- [ ] 监控告警正常工作
- [ ] 回滚方案经过测试
- [ ] 文档已更新

---

**文档状态**: [草稿/评审通过/已验证]  
**合规等级**: [A/B/C]  
**风险评估**: [低/中/高]  
**最后更新**: [更新日期]  
**更新人**: [更新者]  
**审核人**: [审核者]  
**批准人**: [批准者]

---

*本RESTful API重构契约文档是后端API重构的核心法律文档，明确定义了重构的边界条件和验收标准。任何偏离本契约的修改都需要经过严格的变更控制流程和风险评估。*

---

**附件**: 
- [API端点详细定义]
- [数据模型映射表]  
- [测试用例完整列表]
- [性能基准测试报告]
- [风险评估详细报告]
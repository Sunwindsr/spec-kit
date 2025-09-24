# API Test Interface Template

**项目名称**: [PROJECT NAME]  
**创建日期**: [DATE]  
**API版本**: [API VERSION]  
**测试状态**: [DRAFT/READY/COMPLETED]

## 概述

此API测试界面用于验证重构后的API接通测试，确保前端能正确调用所有后端API端点并处理真实数据。

**测试目标**:
- 验证所有API端点的连通性
- 确认前后端数据交互正确
- 验证认证和授权机制
- 测试错误处理和边界情况
- 确保性能达到预期要求

---

## API端点清单

### 基础信息API

| 端点 | 方法 | 功能 | 测试状态 | 备注 |
|------|------|------|----------|------|
| `/api/health` | GET | 系统健康检查 | ☐ 未测试 |  |
| `/api/version` | GET | 版本信息 | ☐ 未测试 |  |
| `/api/config` | GET | 配置信息 | ☐ 未测试 |  |

### 认证授权API

| 端点 | 方法 | 功能 | 测试状态 | 备注 |
|------|------|------|----------|------|
| `/api/auth/login` | POST | 用户登录 | ☐ 未测试 |  |
| `/api/auth/logout` | POST | 用户登出 | ☐ 未测试 |  |
| `/api/auth/refresh` | POST | 刷新令牌 | ☐ 未测试 |  |
| `/api/auth/profile` | GET | 用户信息 | ☐ 未测试 |  |

### 核心业务API

| 端点 | 方法 | 功能 | 测试状态 | 备注 |
|------|------|------|----------|------|
| `/api/[resource]/list` | GET | 获取列表 | ☐ 未测试 |  |
| `/api/[resource]/get/{id}` | GET | 获取详情 | ☐ 未测试 |  |
| `/api/[resource]/create` | POST | 创建资源 | ☐ 未测试 |  |
| `/api/[resource]/update/{id}` | PUT | 更新资源 | ☐ 未测试 |  |
| `/api/[resource]/delete/{id}` | DELETE | 删除资源 | ☐ 未测试 |  |

### 文件操作API

| 端点 | 方法 | 功能 | 测试状态 | 备注 |
|------|------|------|----------|------|
| `/api/files/upload` | POST | 文件上传 | ☐ 未测试 |  |
| `/api/files/download/{id}` | GET | 文件下载 | ☐ 未测试 |  |
| `/api/files/delete/{id}` | DELETE | 文件删除 | ☐ 未测试 |  |

---

## 测试界面设计

### 主界面组件

```typescript
@Component({
  selector: 'api-test-interface',
  template: `
    <div class="api-test-container">
      <!-- 端点选择器 -->
      <div class="endpoint-selector">
        <h3>API端点选择</h3>
        <select [(ngModel)]="selectedEndpoint" (change)="onEndpointChange()">
          <option *ngFor="let endpoint of endpoints" [value]="endpoint.path">
            {{endpoint.method}} {{endpoint.path}} - {{endpoint.description}}
          </option>
        </select>
      </div>

      <!-- 认证设置 -->
      <div class="auth-section">
        <h3>认证设置</h3>
        <input type="text" [(ngModel)]="authToken" placeholder="Auth Token">
        <button (click)="testAuth()">测试认证</button>
      </div>

      <!-- 参数配置 -->
      <div class="params-section">
        <h3>请求参数</h3>
        <div *ngFor="let param of currentEndpoint.params">
          <label>{{param.name}} ({{param.type}})</label>
          <input [type]="param.type === 'number' ? 'number' : 'text'" 
                 [(ngModel)]="paramValues[param.name]">
        </div>
      </div>

      <!-- 请求体配置 -->
      <div class="body-section" *ngIf="currentEndpoint.method !== 'GET'">
        <h3>请求体</h3>
        <textarea [(ngModel)]="requestBody" rows="10"></textarea>
      </div>

      <!-- 执行测试 -->
      <div class="action-section">
        <button (click)="executeTest()" [disabled]="isTesting">
          {{isTesting ? '测试中...' : '执行测试'}}
        </button>
        <button (click)="clearResults()">清空结果</button>
      </div>

      <!-- 测试结果 -->
      <div class="results-section" *ngIf="testResult">
        <h3>测试结果</h3>
        <div class="result-info">
          <span>状态: {{testResult.status}}</span>
          <span>耗时: {{testResult.duration}}ms</span>
          <span>时间: {{testResult.timestamp | date:'yyyy-MM-dd HH:mm:ss'}}</span>
        </div>
        
        <div class="request-info">
          <h4>请求信息</h4>
          <pre>{{testResult.request | json}}</pre>
        </div>

        <div class="response-info">
          <h4>响应信息</h4>
          <pre>{{testResult.response | json}}</pre>
        </div>

        <div class="validation-result">
          <h4>验证结果</h4>
          <div [class]="testResult.valid ? 'valid' : 'invalid'">
            {{testResult.valid ? '✅ 验证通过' : '❌ 验证失败'}}
          </div>
          <div *ngIf="testResult.validationMessage">
            {{testResult.validationMessage}}
          </div>
        </div>
      </div>
    </div>
  `
})
export class ApiTestInterfaceComponent implements OnInit {
  // 端点配置
  endpoints: ApiEndpoint[] = [
    // 从API端点清单自动生成
  ];

  selectedEndpoint: string = '';
  currentEndpoint: ApiEndpoint | null = null;
  authToken: string = '';
  paramValues: any = {};
  requestBody: string = '';
  isTesting: boolean = false;
  testResult: TestResult | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadEndpoints();
  }

  onEndpointChange() {
    this.currentEndpoint = this.endpoints.find(e => e.path === this.selectedEndpoint) || null;
    this.resetTest();
  }

  async executeTest() {
    if (!this.currentEndpoint) return;

    this.isTesting = true;
    const startTime = Date.now();

    try {
      const response = await this.makeApiCall();
      const duration = Date.now() - startTime;
      
      this.testResult = {
        status: response.status,
        duration,
        timestamp: new Date(),
        request: this.buildRequestInfo(),
        response: response.data,
        valid: this.validateResponse(response),
        validationMessage: this.getValidationMessage(response)
      };
    } catch (error) {
      this.testResult = {
        status: 'ERROR',
        duration: Date.now() - startTime,
        timestamp: new Date(),
        request: this.buildRequestInfo(),
        response: error,
        valid: false,
        validationMessage: `请求失败: ${error.message}`
      };
    } finally {
      this.isTesting = false;
    }
  }

  private async makeApiCall() {
    const config = {
      headers: { 'Authorization': `Bearer ${this.authToken}` }
    };

    switch (this.currentEndpoint!.method) {
      case 'GET':
        return this.apiService.get(this.currentEndpoint!.path, this.paramValues, config);
      case 'POST':
        return this.apiService.post(this.currentEndpoint!.path, JSON.parse(this.requestBody), config);
      case 'PUT':
        return this.apiService.put(this.currentEndpoint!.path, this.paramValues, JSON.parse(this.requestBody), config);
      case 'DELETE':
        return this.apiService.delete(this.currentEndpoint!.path, this.paramValues, config);
      default:
        throw new Error(`不支持的HTTP方法: ${this.currentEndpoint!.method}`);
    }
  }

  private validateResponse(response: any): boolean {
    // 验证响应状态码
    if (response.status < 200 || response.status >= 300) {
      return false;
    }

    // 验证响应数据结构
    if (!response.data) {
      return false;
    }

    // 根据端点类型进行特定验证
    return this.validateByEndpointType(response.data);
  }

  private validateByEndpointType(data: any): boolean {
    // 根据不同端点类型实现具体的验证逻辑
    return true;
  }

  private getValidationMessage(response: any): string {
    if (this.testResult?.valid) {
      return 'API调用成功，响应数据格式正确';
    } else {
      return `验证失败: ${response.message || '未知错误'}`;
    }
  }
}
```

---

## 测试用例

### 连通性测试

```typescript
describe('API Connectivity Tests', () => {
  it('should connect to health endpoint', async () => {
    const response = await axios.get('/api/health');
    expect(response.status).toBe(200);
    expect(response.data.status).toBe('healthy');
  });

  it('should authenticate successfully', async () => {
    const response = await axios.post('/api/auth/login', {
      username: 'testuser',
      password: 'testpass'
    });
    expect(response.status).toBe(200);
    expect(response.data.token).toBeDefined();
  });
});
```

### 数据完整性测试

```typescript
describe('API Data Integrity Tests', () => {
  it('should create and retrieve resource', async () => {
    // 创建资源
    const createResponse = await axios.post('/api/resources', {
      name: 'Test Resource',
      value: 'Test Value'
    });
    expect(createResponse.status).toBe(201);
    
    const resourceId = createResponse.data.id;
    
    // 获取资源
    const getResponse = await axios.get(`/api/resources/${resourceId}`);
    expect(getResponse.status).toBe(200);
    expect(getResponse.data.name).toBe('Test Resource');
    expect(getResponse.data.value).toBe('Test Value');
  });

  it('should validate data schema', async () => {
    const response = await axios.get('/api/resources');
    expect(response.status).toBe(200);
    
    response.data.forEach(item => {
      expect(item).toHaveProperty('id');
      expect(item).toHaveProperty('name');
      expect(item).toHaveProperty('createdAt');
    });
  });
});
```

### 错误处理测试

```typescript
describe('API Error Handling Tests', () => {
  it('should handle 404 errors', async () => {
    try {
      await axios.get('/api/nonexistent-endpoint');
      fail('Should have thrown an error');
    } catch (error) {
      expect(error.response.status).toBe(404);
    }
  });

  it('should handle validation errors', async () => {
    try {
      await axios.post('/api/resources', {
        name: '', // 无效的空名称
        value: 'Test Value'
      });
      fail('Should have thrown a validation error');
    } catch (error) {
      expect(error.response.status).toBe(400);
      expect(error.response.data.errors).toBeDefined();
    }
  });
});
```

---

## 测试检查清单

### 通用检查项
- [ ] 所有API端点已在测试界面中注册
- [ ] 认证机制配置正确
- [ ] 请求参数验证逻辑实现
- [ ] 响应数据验证逻辑实现
- [ ] 错误处理机制完善

### 连通性检查项
- [ ] 所有GET端点返回200状态码
- [ ] 所有POST端点能成功创建数据
- [ ] 所有PUT端点能成功更新数据
- [ ] 所有DELETE端点能成功删除数据
- [ ] API响应时间在可接受范围内

### 数据质量检查项
- [ ] 返回数据结构符合预期
- [ ] 数据类型和格式正确
- [ ] 必填字段验证正常工作
- [ ] 业务逻辑验证正常工作
- [ ] 数据关联关系正确

### 安全性检查项
- [ ] 未认证请求被正确拒绝
- [ ] 权限控制机制正常工作
- [ ] 敏感数据不被意外泄露
- [ ] 输入验证和SQL注入防护
- [ ] CORS配置正确

---

## 部署说明

### 开发环境部署
1. 将测试界面组件添加到开发环境
2. 配置开发环境的API地址
3. 确保CORS允许开发环境访问
4. 运行测试界面验证所有端点

### 测试环境部署
1. 将测试界面部署到测试环境
2. 配置测试环境的API地址
3. 使用测试数据执行完整测试
4. 生成测试报告并验证结果

### 生产环境注意事项
- 生产环境不应部署测试界面
- 可考虑在生产环境部署只读的健康检查端点
- 确保测试接口不会影响生产数据

---

## 测试报告模板

### 测试执行摘要
**执行时间**: [DATETIME]  
**测试环境**: [ENVIRONMENT]  
**测试人员**: [TESTER]  
**API版本**: [VERSION]  

### 测试结果统计
- **总端点数量**: [TOTAL]
- **测试通过**: [PASSED]
- **测试失败**: [FAILED]
- **成功率**: [PERCENTAGE]%

### 失败端点详情
| 端点 | 错误描述 | 解决状态 |
|------|----------|----------|
| [ENDPOINT] | [ERROR] | [STATUS] |

### 性能指标
- **平均响应时间**: [TIME]ms
- **最快响应时间**: [TIME]ms
- **最慢响应时间**: [TIME]ms
- **95%响应时间**: [TIME]ms

### 建议措施
- [高优先级] 立即修复失败的端点
- [中优先级] 优化慢响应端点
- [低优先级] 完善错误处理机制

---

*此模板为API接通测试的标准化工具，确保重构后的API能正确处理前端请求*
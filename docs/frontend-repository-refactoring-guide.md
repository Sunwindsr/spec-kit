# 前端重构Repository层特殊要求指南

## 概述

本指南专门针对前端项目重构中的Repository层精准还原要求，基于Constitution VI-G原则，确保前端项目重构过程中数据访问层的100%精准还原。

## 适用范围

- **前端技术栈重构**: React/Vue/Angular等框架的完整替换
- **数据访问层重构**: API调用层、数据服务层的重构
- **状态管理重构**: Redux/Zustand/MobX等状态管理库的替换

## 核心原则

### 1. API调用模式必须100%保持 (P0)

#### HTTP请求规范
```typescript
// 源系统API调用模式 - 必须完全保持
const getUserData = async (userId: string): Promise<User> => {
  const response = await fetch(`/api/users/${userId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });
  return response.json();
};

// 重构后必须保持完全相同的调用模式
// 严禁修改：HTTP方法、URL路径、请求头、查询参数
```

#### API端点映射表
| 功能 | HTTP方法 | URL路径 | 必须保持 |
|------|----------|---------|----------|
| 获取用户信息 | GET | `/api/users/{id}` | ✅ 必须保持 |
| 创建用户 | POST | `/api/users` | ✅ 必须保持 |
| 更新用户 | PUT | `/api/users/{id}` | ✅ 必须保持 |
| 删除用户 | DELETE | `/api/users/{id}` | ✅ 必须保持 |

### 2. 数据加载策略必须完全一致 (P0)

#### 懒加载策略
```typescript
// 源系统懒加载实现
const UserProfile = () => {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    // 必须保持相同的懒加载时机
    const loadUser = async () => {
      const userData = await userService.getUser();
      setUser(userData);
    };
    
    // 仅在组件挂载时加载
    loadUser();
  }, []); // 依赖数组必须保持完全一致
  
  return <div>{user?.name}</div>;
};
```

#### 分页加载策略
```typescript
// 源系统分页加载实现
const loadUsers = async (page: number, pageSize: number) => {
  const response = await fetch(`/api/users?page=${page}&size=${pageSize}`);
  return {
    data: await response.json(),
    total: parseInt(response.headers.get('X-Total-Count') || '0'),
    page,
    pageSize
  };
};

// 重构后必须保持：
// 1. 相同的分页参数结构
// 2. 相同的响应格式
// 3. 相同的页码计算逻辑
```

### 3. 错误处理机制必须完全相同 (P0)

#### 网络错误处理
```typescript
// 源系统错误处理模式
const fetchUserData = async (userId: string) => {
  try {
    const response = await fetch(`/api/users/${userId}`);
    
    if (!response.ok) {
      // HTTP错误状态处理必须保持
      if (response.status === 404) {
        throw new Error('User not found');
      } else if (response.status === 401) {
        throw new Error('Unauthorized access');
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    // 错误类型和消息必须完全保持
    console.error('Failed to fetch user:', error);
    throw error;
  }
};
```

#### 业务错误处理
```typescript
// 源系统业务错误处理
const createUser = async (userData: CreateUserRequest) => {
  try {
    const user = await userService.createUser(userData);
    return user;
  } catch (error) {
    // 业务错误消息必须完全保持
    if (error.message.includes('Email already exists')) {
      setError('email', '该邮箱已被注册');
    } else if (error.message.includes('Invalid phone number')) {
      setError('phone', '手机号码格式不正确');
    }
    throw error;
  }
};
```

### 4. 数据转换逻辑必须保持不变 (P0)

#### 响应数据转换
```typescript
// 源系统数据转换逻辑
const transformUserResponse = (response: any): User => {
  return {
    id: response.id,
    name: response.full_name, // 字段映射必须保持
    email: response.email_address.toLowerCase(), // 数据处理必须保持
    avatar: response.profile_image_url || '/default-avatar.png', // 默认值逻辑必须保持
    createdAt: new Date(response.created_at), // 日期转换必须保持
    updatedAt: response.updated_at ? new Date(response.updated_at) : null
  };
};

// 重构后必须保持完全相同的转换逻辑
// 严禁修改字段映射、数据处理、默认值逻辑
```

### 5. 状态管理模式必须完全保持 (P0)

#### 状态管理行为
```typescript
// 源系统状态管理模式
const useUserStore = (set, get) => ({
  users: [],
  currentUser: null,
  loading: false,
  error: null,
  
  // 状态更新机制必须保持
  setUsers: (users) => set({ users }),
  setCurrentUser: (user) => set({ currentUser: user }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  
  // 异步操作模式必须保持
  fetchUsers: async () => {
    set({ loading: true, error: null });
    try {
      const users = await userService.getUsers();
      set({ users, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  }
});
```

#### 响应式行为保持
```typescript
// 源系统响应式行为
const UserList = () => {
  const { users, loading, error, fetchUsers } = useUserStore();
  
  // 依赖数组和副作用时机必须保持
  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
};
```

## 验证标准

### 1. 功能一致性验证

#### 测试用例要求
```typescript
// 必须编写的验证测试
describe('Repository Layer Consistency', () => {
  it('should maintain exact API call patterns', async () => {
    // 监控API调用
    const mockFetch = jest.fn();
    global.fetch = mockFetch;
    
    // 执行源系统操作
    await sourceRepository.getUser('123');
    
    // 执行重构后操作
    await refactoredRepository.getUser('123');
    
    // 验证调用模式完全一致
    expect(mockFetch.mock.calls).toEqual([
      ['/api/users/123', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test-token'
        }
      }]
    ]);
  });
  
  it('should maintain identical error handling', async () => {
    // 模拟相同的错误场景
    mockFetch.mockRejectedValueOnce(new Error('Network error'));
    
    // 验证错误处理行为完全一致
    await expect(sourceRepository.getUser('123')).rejects.toThrow('Network error');
    await expect(refactoredRepository.getUser('123')).rejects.toThrow('Network error');
  });
});
```

### 2. 性能特征验证

#### 响应时间验证
```typescript
// 性能基准测试
describe('Performance Consistency', () => {
  it('should maintain similar response times', async () => {
    const sourceTimes = [];
    const refactoredTimes = [];
    
    // 执行多次测试
    for (let i = 0; i < 10; i++) {
      const sourceStart = performance.now();
      await sourceRepository.getUser('123');
      sourceTimes.push(performance.now() - sourceStart);
      
      const refactoredStart = performance.now();
      await refactoredRepository.getUser('123');
      refactoredTimes.push(performance.now() - refactoredStart);
    }
    
    // 计算平均响应时间
    const sourceAvg = sourceTimes.reduce((a, b) => a + b) / sourceTimes.length;
    const refactoredAvg = refactoredTimes.reduce((a, b) => a + b) / refactoredTimes.length;
    
    // 验证性能差异在可接受范围内 (±10%)
    expect(Math.abs(sourceAvg - refactoredAvg) / sourceAvg).toBeLessThan(0.1);
  });
});
```

## 违规后果

### 严重违规（立即重构）
- 修改API调用模式（HTTP方法、URL、请求头）
- 改变数据加载策略或时机
- 修改错误处理机制或错误消息
- 改变状态管理行为或响应式逻辑

### 中度违规（需要修复）
- 性能差异超过允许范围
- 数据转换逻辑不一致
- 缓存策略不匹配

### 轻度违规（建议优化）
- 代码风格不一致
- 注释不完整

## 工具支持

### 自动化验证脚本
```bash
# 运行Repository层验证
python scripts/validate-repository-layer.py \
  /path/to/source/frontend \
  /path/to/refactored/frontend \
  --output validation_report.json \
  --format json
```

### 检查清单
- [ ] 所有API调用模式完全保持
- [ ] 数据加载策略完全一致
- [ ] 错误处理机制完全相同
- [ ] 数据转换逻辑保持不变
- [ ] 状态管理模式完全保持
- [ ] 性能特征在可接受范围内
- [ ] 所有验证测试通过

## 总结

前端重构中的Repository层精准还原是确保系统行为一致性的关键。所有数据访问相关的逻辑必须100%保持原有行为，任何变更都必须经过严格验证和测试。

**记住**: 前端重构允许UI/UX的现代化改进，但数据访问层的行为必须完全保持不变。
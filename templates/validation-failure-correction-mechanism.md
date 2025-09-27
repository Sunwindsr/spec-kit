# 验证失败纠正机制

## 纠正机制设计原则

### 核心原则
1. **自动识别**: 系统自动识别验证失败的具体原因
2. **智能分析**: 分析失败的根本原因和影响范围
3. **具体建议**: 提供可执行的纠正措施
4. **持续改进**: 通过失败学习改进验证规则

### 纠正流程架构
```typescript
interface ValidationCorrectionSystem {
  // 失败识别
  identifyValidationFailure(validationResult: ValidationResult): ValidationIssue[];
  
  // 根本原因分析
  analyzeRootCause(issues: ValidationIssue[]): RootCauseAnalysis;
  
  // 纠正建议生成
  generateCorrectionPlan(analysis: RootCauseAnalysis): CorrectionPlan;
  
  // 纠正执行
  executeCorrections(plan: CorrectionPlan): CorrectionResult;
  
  // 重新验证
  revalidateAfterCorrection(taskId: string): ValidationResult;
}
```

## 验证失败类型和纠正策略

### 1. Task创建失败纠正

#### 失败类型: MISSING_FR_ASSOCIATION
```typescript
interface MissingFRIssue extends ValidationIssue {
  code: 'MISSING_FR_ASSOCIATION';
  taskId: string;
  message: 'Task没有关联FR ID';
  severity: 'CRITICAL';
}

// 纠正策略
const missingFRCorrection: CorrectionAction = {
  type: 'ADD_FR_ASSOCIATION',
  description: '为Task关联相应的FR ID',
  priority: 'HIGH',
  estimatedTime: 30, // 分钟
  steps: [
    '分析Task描述确定功能范围',
    '查找相关的FR文档',
    '建立Task-FR关联关系',
    '验证关联的正确性'
  ]
};
```

#### 失败类型: MISSING_TESTCASES
```typescript
interface MissingTestcaseIssue extends ValidationIssue {
  code: 'MISSING_TESTCASES';
  taskId: string;
  requiredCount: number;
  actualCount: number;
  message: 'Task没有足够的Testcase';
  severity: 'CRITICAL';
}

// 纠正策略
const missingTestcaseCorrection: CorrectionAction = {
  type: 'ADD_TESTCASE',
  description: '为Task生成缺失的Testcase',
  priority: 'HIGH',
  estimatedTime: 60,
  steps: [
    '分析Task的验收标准',
    '识别关键测试场景',
    '生成Testcase模板',
    '定义Expected Result',
    '建立Testcase-Task关联'
  ]
};
```

### 2. Task执行失败纠正

#### 失败类型: DEPENDENCIES_NOT_COMPLETE
```typescript
interface DependencyIssue extends ValidationIssue {
  code: 'DEPENDENCIES_NOT_COMPLETE';
  taskId: string;
  incompleteDeps: string[];
  message: '依赖任务未完成';
  severity: 'MAJOR';
}

// 纠正策略
const dependencyCorrection: CorrectionAction = {
  type: 'WAIT_FOR_DEPENDENCIES',
  description: '等待依赖任务完成',
  priority: 'HIGH',
  estimatedTime: 120,
  steps: [
    '识别未完成的依赖任务',
    '联系相关开发人员',
    '监控依赖任务状态',
    '依赖完成后重新执行'
  ]
};
```

#### 失败类型: RESOURCE_LIMIT_EXCEEDED
```typescript
interface ResourceIssue extends ValidationIssue {
  code: 'RESOURCE_LIMIT_EXCEEDED';
  taskId: string;
  resourceType: 'MEMORY' | 'CPU' | 'TIME';
  actualUsage: number;
  limit: number;
  message: '资源使用超过限制';
  severity: 'MAJOR';
}

// 纠正策略
const resourceCorrection: CorrectionAction = {
  type: 'OPTIMIZE_RESOURCE_USAGE',
  description: '优化资源使用',
  priority: 'MEDIUM',
  estimatedTime: 90,
  steps: [
    '分析资源使用瓶颈',
    '优化算法和数据结构',
    '添加资源监控',
    '调整资源限制'
  ]
};
```

### 3. Task完成失败纠正

#### 失败类型: TESTCASES_FAILED
```typescript
interface FailedTestcaseIssue extends ValidationIssue {
  code: 'TESTCASES_FAILED';
  taskId: string;
  failedTestcases: string[];
  failureDetails: TestFailureDetail[];
  message: '有Testcase执行失败';
  severity: 'CRITICAL';
}

// 纠正策略
const failedTestcaseCorrection: CorrectionAction = {
  type: 'FIX_FAILED_TESTCASES',
  description: '修复失败的Testcase',
  priority: 'HIGH',
  estimatedTime: 180,
  steps: [
    '分析Testcase失败原因',
    '检查代码逻辑',
    '修复实现问题',
    '重新运行Testcase',
    '验证修复效果'
  ]
};
```

## 纠正机制实现

### 纠正建议生成器
```typescript
class CorrectionSuggestionGenerator {
  generateSuggestions(issues: ValidationIssue[]): CorrectionPlan {
    const corrections: CorrectionAction[] = [];
    
    for (const issue of issues) {
      const suggestion = this.generateSuggestionForIssue(issue);
      if (suggestion) {
        corrections.push(suggestion);
      }
    }
    
    return {
      taskId: issues[0]?.taskId || '',
      issues,
      corrections,
      verificationSteps: this.generateVerificationSteps(issues),
      estimatedTotalTime: corrections.reduce((sum, c) => sum + c.estimatedTime, 0)
    };
  }
  
  private generateSuggestionForIssue(issue: ValidationIssue): CorrectionAction | null {
    switch (issue.code) {
      case 'MISSING_FR_ASSOCIATION':
        return this.createFRAssociationSuggestion(issue);
      case 'MISSING_TESTCASES':
        return this.createTestcaseSuggestion(issue);
      case 'TESTCASES_FAILED':
        return this.createFailedTestcaseSuggestion(issue);
      case 'DEPENDENCIES_NOT_COMPLETE':
        return this.createDependencySuggestion(issue);
      default:
        return this.createGenericSuggestion(issue);
    }
  }
  
  private createFRAssociationSuggestion(issue: ValidationIssue): CorrectionAction {
    return {
      type: 'ADD_FR_ASSOCIATION',
      description: `为Task ${issue.taskId} 关联相应的FR ID`,
      priority: 'HIGH',
      estimatedTime: 30,
      steps: [
        '1. 分析Task描述确定功能范围',
        '2. 在FR文档中查找相关功能需求',
        '3. 建立Task-FR关联关系',
        '4. 验证关联的业务逻辑一致性'
      ]
    };
  }
  
  private createTestcaseSuggestion(issue: ValidationIssue): CorrectionAction {
    const missingIssue = issue as MissingTestcaseIssue;
    const neededCount = missingIssue.requiredCount - missingIssue.actualCount;
    
    return {
      type: 'ADD_TESTCASE',
      description: `为Task ${issue.taskId} 生成${neededCount}个缺失的Testcase`,
      priority: 'HIGH',
      estimatedTime: neededCount * 30,
      steps: [
        '1. 分析Task的验收标准和业务逻辑',
        '2. 识别关键测试场景和边界情况',
        '3. 为每个场景生成Testcase模板',
        '4. 定义清晰的Expected Result',
        '5. 建立Testcase-Task关联关系'
      ]
    };
  }
  
  private createFailedTestcaseSuggestion(issue: ValidationIssue): CorrectionAction {
    const failedIssue = issue as FailedTestcaseIssue;
    
    return {
      type: 'FIX_FAILED_TESTCASES',
      description: `修复Task ${issue.taskId} 中失败的${failedIssue.failedTestcases.length}个Testcase`,
      priority: 'HIGH',
      estimatedTime: failedIssue.failedTestcases.length * 60,
      steps: [
        '1. 分析每个Testcase失败的具体原因',
        '2. 检查相关代码的实现逻辑',
        '3. 修复导致失败的技术问题',
        '4. 重新运行失败的Testcase',
        '5. 验证所有相关功能仍正常工作'
      ]
    };
  }
}
```

### 纠正执行引擎
```typescript
class CorrectionExecutionEngine {
  async executeCorrections(plan: CorrectionPlan): Promise<CorrectionResult> {
    const results: CorrectionActionResult[] = [];
    
    for (const correction of plan.corrections) {
      try {
        const result = await this.executeSingleCorrection(correction);
        results.push(result);
      } catch (error) {
        results.push({
          correction,
          success: false,
          error: error.message,
          executionTime: 0
        });
      }
    }
    
    return {
      planId: plan.taskId,
      results,
      success: results.every(r => r.success),
      totalExecutionTime: results.reduce((sum, r) => sum + r.executionTime, 0)
    };
  }
  
  private async executeSingleCorrection(correction: CorrectionAction): Promise<CorrectionActionResult> {
    const startTime = Date.now();
    
    switch (correction.type) {
      case 'ADD_FR_ASSOCIATION':
        return await this.executeFRAssociationCorrection(correction);
      case 'ADD_TESTCASE':
        return await this.executeTestcaseCorrection(correction);
      case 'FIX_FAILED_TESTCASES':
        return await this.executeTestcaseFixCorrection(correction);
      default:
        throw new Error(`Unknown correction type: ${correction.type}`);
    }
  }
  
  private async executeFRAssociationCorrection(correction: CorrectionAction): Promise<CorrectionActionResult> {
    // 实现FR关联纠正逻辑
    console.log(`Executing FR association correction: ${correction.description}`);
    
    // 1. 分析Task描述
    const taskAnalysis = await this.analyzeTaskDescription(correction.taskId);
    
    // 2. 查找相关FR
    const relatedFRs = await this.findRelatedFRs(taskAnalysis);
    
    // 3. 建立关联
    if (relatedFRs.length > 0) {
      await this.establishTaskFRAssociation(correction.taskId, relatedFRs[0]);
      return {
        correction,
        success: true,
        message: `Successfully associated FR ${relatedFRs[0].id} with task ${correction.taskId}`,
        executionTime: Date.now() - startTime
      };
    } else {
      return {
        correction,
        success: false,
        error: 'No related FRs found',
        executionTime: Date.now() - startTime
      };
    }
  }
  
  private async executeTestcaseCorrection(correction: CorrectionAction): Promise<CorrectionActionResult> {
    // 实现Testcase生成纠正逻辑
    console.log(`Executing testcase correction: ${correction.description}`);
    
    // 1. 分析Task需求
    const taskRequirements = await this.analyzeTaskRequirements(correction.taskId);
    
    // 2. 生成Testcase
    const generatedTestcases = await this.generateTestcases(taskRequirements);
    
    // 3. 建立关联
    for (const testcase of generatedTestcases) {
      await this.establishTestcaseTaskAssociation(testcase.id, correction.taskId);
    }
    
    return {
      correction,
      success: true,
      message: `Generated ${generatedTestcases.length} testcases for task ${correction.taskId}`,
      executionTime: Date.now() - startTime
    };
  }
}
```

## 验证失败恢复机制

### 自动恢复策略
```typescript
interface RecoveryStrategy {
  strategy: 'AUTOMATIC' | 'MANUAL' | 'HYBRID';
  maxRetries: number;
  retryDelay: number;
  escalationConditions: string[];
}

class ValidationRecoveryManager {
  private strategies: Map<string, RecoveryStrategy> = new Map();
  
  constructor() {
    this.initializeStrategies();
  }
  
  private initializeStrategies() {
    this.strategies.set('MISSING_FR_ASSOCIATION', {
      strategy: 'MANUAL',
      maxRetries: 3,
      retryDelay: 300000, // 5分钟
      escalationConditions: ['no_related_fr_found']
    });
    
    this.strategies.set('MISSING_TESTCASES', {
      strategy: 'HYBRID',
      maxRetries: 2,
      retryDelay: 180000, // 3分钟
      escalationConditions: ['cannot_generate_testcases']
    });
    
    this.strategies.set('TESTCASES_FAILED', {
      strategy: 'AUTOMATIC',
      maxRetries: 5,
      retryDelay: 60000, // 1分钟
      escalationConditions: ['persistent_failures']
    });
  }
  
  async handleValidationFailure(taskId: string, validationResult: ValidationResult): Promise<boolean> {
    const strategy = this.selectRecoveryStrategy(validationResult);
    
    switch (strategy.strategy) {
      case 'AUTOMATIC':
        return await this.handleAutomaticRecovery(taskId, validationResult, strategy);
      case 'MANUAL':
        return await this.handleManualRecovery(taskId, validationResult, strategy);
      case 'HYBRID':
        return await this.handleHybridRecovery(taskId, validationResult, strategy);
    }
  }
  
  private async handleAutomaticRecovery(taskId: string, validationResult: ValidationResult, strategy: RecoveryStrategy): Promise<boolean> {
    let retryCount = 0;
    
    while (retryCount < strategy.maxRetries) {
      try {
        // 生成纠正计划
        const correctionPlan = await this.generateCorrectionPlan(validationResult);
        
        // 执行纠正
        const correctionResult = await this.executeCorrections(correctionPlan);
        
        if (correctionResult.success) {
          // 重新验证
          const newValidation = await this.revalidateTask(taskId);
          if (newValidation.isValid) {
            return true;
          }
        }
        
        retryCount++;
        await this.delay(strategy.retryDelay);
      } catch (error) {
        retryCount++;
        await this.delay(strategy.retryDelay);
      }
    }
    
    return false;
  }
}
```

## 纠正效果评估

### 评估指标
```typescript
interface CorrectionMetrics {
  totalCorrections: number;
  successfulCorrections: number;
  failedCorrections: number;
  averageCorrectionTime: number;
  correctionSuccessRate: number;
  mostCommonIssues: string[];
  improvementSuggestions: string[];
}

class CorrectionEffectivenessAnalyzer {
  analyzeCorrectionEffectiveness(corrections: CorrectionResult[]): CorrectionMetrics {
    const total = corrections.length;
    const successful = corrections.filter(c => c.success).length;
    const failed = total - successful;
    const totalTime = corrections.reduce((sum, c) => sum + c.totalExecutionTime, 0);
    
    // 分析最常见的问题
    const issueFrequency = this.analyzeIssueFrequency(corrections);
    
    return {
      totalCorrections: total,
      successfulCorrections: successful,
      failedCorrections: failed,
      averageCorrectionTime: totalTime / total,
      correctionSuccessRate: (successful / total) * 100,
      mostCommonIssues: issueFrequency,
      improvementSuggestions: this.generateImprovementSuggestions(issueFrequency)
    };
  }
  
  private generateImprovementSuggestions(commonIssues: string[]): string[] {
    const suggestions: string[] = [];
    
    if (commonIssues.includes('MISSING_TESTCASES')) {
      suggestions.push('建议在Task创建阶段强制要求Testcase关联');
    }
    
    if (commonIssues.includes('TESTCASES_FAILED')) {
      suggestions.push('建议加强代码审查和测试质量');
    }
    
    if (commonIssues.includes('MISSING_FR_ASSOCIATION')) {
      suggestions.push('建议改进FR文档的可发现性');
    }
    
    return suggestions;
  }
}
```

这个纠正机制提供了完整的验证失败处理流程，包括自动识别、智能分析、具体建议和持续改进，确保系统能够从验证失败中学习并不断完善。
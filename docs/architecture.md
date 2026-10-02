# 逻辑架构

```mermaid
flowchart TD
  A[领号 OBD-六位] --> B[字形指针]
  B --> C[组类层]
  B --> D[辞例层 双人录入]
  C --> E[形式门 自动校验]
  D --> E
  F[候选接口 machine-suggestion] -.->|不得写入证据| E
  E --> G[社区复核与排序]
  G --> H[14 天反证期]
  H --> I{专家档是否启用}
  I -->|否 当前| J[停在可接受的候选或更低]
  I -->|是 尚未| K[专家认可]
  K --> L[报告模板]
  L --> M[中国文字博物馆 投递待补充]
```

数据流：

1. 领号。测试段 OBD-900001 至 OBD-900099 跳过。
2. 字形层只存指针、来源、摹写状态、疑似关系。
3. 组类层存分期组类。新手不写终判。
4. 辞例层存自录释文。双录比对。
5. 候选接口读指针，写出带 `machine-suggestion` 的记录并写日志。档案的证据字段不能引用它。
6. 形式门校验 Schema、编号、辞例封顶、图像与域名、试点日志。
7. 社区票只排序。
8. 反证期结束且没有未回应的实质反例，才可能到“可接受的候选”。
9. “专家认可”空置。报告模板因此不会进入发送。
10. 演练日志在 `pilot/_drill/`。校验会跑，发布和统计排除该目录。

crosswalk 单独存放外部字头对应，可后补。

## English

Registration is pointers, not images. Model output is logged and cannot be cited as evidence. Drill logs are validated and then left out of published counts.

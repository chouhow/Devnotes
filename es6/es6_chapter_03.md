# 第三章：模板字符串与解构赋值

> 如果把 JavaScript 比作一辆不断升级迭代的汽车，那么 ES6 就是一次脱胎换骨的大改款。在这一章里，我们要认识两位贴心的"行车助手"——**模板字符串**（让你的字符串操作告别繁琐）和**解构赋值**（让数据提取变得优雅从容）。让我们系好安全带，出发！

---

## 3.1 模板字符串：字符串的升级补丁

### 3.1.1 为什么需要模板字符串？

想象一下，你在拼装一段带有变量的文字，就像用乐高积木拼接一个复杂模型——每一块（变量）都要小心翼翼地用 `+` 号连接起来，稍有不慎就会拼错。ES5 时代的字符串拼接，写起来又丑又容易出错：

```javascript
// ES5：拼接一段用户信息
var name = '小明';
var age = 18;
var hobby = '打篮球';

var info = '大家好，我叫' + name + '，今年' + age + '岁，我喜欢' + hobby + '。';
console.log(info);
// 输出结果：大家好，我叫小明，今年18岁，我喜欢打篮球。
```

这串代码里的加号 `+` 就像一颗颗散落的钉子，不仅要记住在变量前后加上，还要时刻留意空格的位置。**ES6 的模板字符串**就像给字符串打了一剂"升级补丁"——用反引号 `` ` `` 包裹，变量直接往里"塞"，代码瞬间清爽了十倍！

### 3.1.2 基本语法

模板字符串使用反引号（`` ` ``，键盘上 Tab 键上方那个键）来包裹内容，变量和表达式则放在 `${...}` 中：

```javascript
// ES6：模板字符串，优雅又直观
const name = '小明';
const age = 18;
const hobby = '打篮球';

const info = `大家好，我叫${name}，今年${age}岁，我喜欢${hobby}。`;
console.log(info);
// 输出结果：大家好，我叫小明，今年18岁，我喜欢打篮球。
```

| 特性 | ES5 拼接 | ES6 模板字符串 |
|:---|:---|:---|
| **引号** | 单/双引号 `'"` | 反引号 `` ` `` |
| **变量插入** | `+` 拼接 | `${变量}` 插值 |
| **可读性** | 加号多、易混乱 | 像填空一样直观 |
| **多行文本** | 需要 `\n` 转义 | 直接回车换行 |

### 3.1.3 多行字符串

在 ES5 中写多行文本，就像在一张小纸条上写长文章——空间不够，只能靠换行符 `\n` 硬撑：

```javascript
// ES5：多行字符串的"痛苦写法"
var poem = '春眠不觉晓，\n'
         + '处处闻啼鸟。\n'
         + '夜来风雨声，\n'
         + '花落知多少。';
console.log(poem);
// 输出结果：
// 春眠不觉晓，
// 处处闻啼鸟。
// 夜来风雨声，
// 花落知多少。
```

模板字符串让多行文本变得像写诗一样自然——直接在代码里换行就行：

```javascript
// ES6：多行字符串，所见即所得
const poem = `春眠不觉晓，
处处闻啼鸟。
夜来风雨声，
花落知多少。`;
console.log(poem);
// 输出结果：
// 春眠不觉晓，
// 处处闻啼鸟。
// 夜来风雨声，
// 花落知多少。
```

**坑点提醒：** 模板字符串会保留所有的空格和缩进。如果你代码里缩进了，输出也会有缩进：

```javascript
function showMessage() {
  // 注意：这行字符串前面有空格！
  const msg = `这是一段
               带缩进的文字`;
  console.log(msg);
  // 输出时"带缩进的文字"前面会有空白字符
}
```

### 3.1.4 字符串插值与表达式

`${...}` 大括号里可不只是能放变量，**任何有效的 JavaScript 表达式**都可以往里塞——算式、三元运算、函数调用，统统没问题！

```javascript
// ES5：表达式拼接
var a = 10;
var b = 20;
var result = '两数之和是：' + (a + b) + '，乘积是：' + (a * b);
console.log(result);
// 输出结果：两数之和是：30，乘积是：600
```

```javascript
// ES6：表达式直接嵌入
const a = 10;
const b = 20;
const result = `两数之和是：${a + b}，乘积是：${a * b}`;
console.log(result);
// 输出结果：两数之和是：30，乘积是：600

// 还能放三元表达式
const score = 85;
const grade = `你的成绩${score >= 60 ? '及格了' : '不及格'}，分数是${score}`;
console.log(grade);
// 输出结果：你的成绩及格了，分数是85

// 甚至能放函数调用
function formatPrice(price) {
  return '¥' + price.toFixed(2);
}
const price = 199.9;
console.log(`商品价格：${formatPrice(price)}`);
// 输出结果：商品价格：¥199.90
```

| 可以在 `${}` 中使用的 | 示例 |
|:---|:---|
| 变量 | `${name}` |
| 算术表达式 | `${a + b}`、 `${price * 0.8}` |
| 三元表达式 | `${age >= 18 ? '成年' : '未成年'}` |
| 函数调用 | `${getFullName()}` |
| 属性访问 | `${user.name}`、 `${arr.length}` |

### 3.1.5 标签模板（Tag Template）

标签模板是模板字符串的"进阶玩法"，它允许你用一个**函数**来处理模板字符串。虽然日常使用不多，但了解它能让你在需要时大显身手。

简单来说，标签模板就像给模板字符串请了一个"私人编辑"——在字符串输出之前，由你来决定如何处理里面的内容。

```javascript
// 标签模板的基本用法
function myTag(strings, ...values) {
  // strings: 模板中被变量分割开的字符串数组
  // values: 所有 ${...} 中的值
  console.log('字符串片段：', strings);
  console.log('变量值：', values);
  
  // 可以在这里对值进行任何处理
  let result = '';
  for (let i = 0; i < strings.length; i++) {
    result += strings[i];
    if (i < values.length) {
      result += `[${values[i]}]`; // 给每个变量值加上方括号
    }
  }
  return result;
}

const name = '小明';
const age = 18;
const output = myTag`姓名：${name}，年龄：${age}岁`;
console.log(output);
// 字符串片段：['姓名：', '，年龄：', '岁']
// 变量值：['小明', 18]
// 输出结果：姓名：[小明]，年龄：[18]岁
```

**实际应用场景——防止 XSS 攻击（转义 HTML）：**

```javascript
// 简单的 HTML 转义标签函数
function safeHtml(strings, ...values) {
  const escape = (str) => str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
  
  let result = strings[0];
  for (let i = 0; i < values.length; i++) {
    result += escape(String(values[i])) + strings[i + 1];
  }
  return result;
}

const userInput = '<script>alert("hack")</script>';
const html = safeHtml`<div>用户评论：${userInput}</div>`;
console.log(html);
// 输出结果：<div>用户评论：&lt;script&gt;alert("hack")&lt;/script&gt;</div>
// 恶意代码被安全转义了！
```

---

## 3.2 解构赋值：自动拆快递包裹

### 3.2.1 为什么需要解构？

想象一下你收到一个快递包裹，里面有一堆你需要的东西。ES5 时代，你只能一件一件往外拿：

```javascript
// ES5：手动"拆包裹"
var user = ['张三', 25, '程序员'];

var name = user[0];
var age = user[1];
var job = user[2];

console.log(name, age, job);
// 输出结果：张三 25 程序员
```

ES6 的解构赋值就像请了一个智能分拣机器人——**按照你规定的格式，自动把包裹里的东西分配到对应的变量上**，一行代码搞定！

### 3.2.2 数组解构

#### 基本解构

```javascript
// ES5：手动提取数组元素
var colors = ['red', 'green', 'blue'];
var first = colors[0];
var second = colors[1];
var third = colors[2];
console.log(first, second, third);
// 输出结果：red green blue
```

```javascript
// ES6：数组解构——左边"画"出想要的结构
const colors = ['red', 'green', 'blue'];
const [first, second, third] = colors;
console.log(first, second, third);
// 输出结果：red green blue
```

解构的本质是"模式匹配"——等号左边的 `[first, second, third]` 描述了你想从右边的数组中提取的结构。

#### 跳过元素

有时候包裹里有些东西你不想要，可以用逗号占位跳过：

```javascript
// 只想要第一个和第三个
const colors = ['red', 'green', 'blue'];
const [first, , third] = colors;  // 注意中间的逗号，跳过第二个
console.log(first, third);
// 输出结果：red blue
```

#### 默认值

如果包裹里某个位置没东西（`undefined`），可以给变量设一个"保底值"：

```javascript
// ES5：手动设置默认值
var user = ['张三'];
var name = user[0] || '匿名';
var age = user[1] || 18;
console.log(name, age);
// 输出结果：张三 18
```

```javascript
// ES6：解构时直接设置默认值
const user = ['张三'];  // 没有提供 age
const [name, age = 18] = user;
console.log(name, age);
// 输出结果：张三 18

// 注意：只有 undefined 才会触发默认值
const data = [null, 0, ''];
const [a = 1, b = 2, c = 3, d = 4] = data;
console.log(a, b, c, d);
// 输出结果：null 0 "" 4
// null、0、空字符串都是有效值，不会被默认值替代
// 只有 data[3] 是 undefined，所以 d = 4
```

#### 剩余元素

用展开运算符 `...` 把剩下的元素全部收入一个新数组：

```javascript
// ES5：获取剩余元素
var nums = [1, 2, 3, 4, 5];
var first = nums[0];
var rest = nums.slice(1);
console.log(first, rest);
// 输出结果：1 [2, 3, 4, 5]
```

```javascript
// ES6：剩余元素解构
const nums = [1, 2, 3, 4, 5];
const [first, ...rest] = nums;
console.log(first, rest);
// 输出结果：1 [2, 3, 4, 5]

// 也可以跳过前面的，收集中间的
const colors = ['red', 'green', 'blue', 'yellow'];
const [, second, ...others] = colors;
console.log(second, others);
// 输出结果：green ['blue', 'yellow']
```

**坑点提醒：** 剩余元素必须是解构模式的最后一个，后面不能再放其他元素！

```javascript
// 错误的写法！
const [a, ...middle, b] = [1, 2, 3, 4, 5];
// SyntaxError: Rest element must be last element
```

### 3.2.3 对象解构

如果说数组解构是按"位置"拆包裹，那对象解构就是按"名字"拆包裹——你告诉机器人要什么东西，它按名称给你找出来。

#### 基本解构

```javascript
// ES5：手动提取对象属性
var user = { name: '张三', age: 25, job: '程序员' };

var name = user.name;
var age = user.age;
var job = user.job;
console.log(name, age, job);
// 输出结果：张三 25 程序员
```

```javascript
// ES6：对象解构——按属性名匹配
const user = { name: '张三', age: 25, job: '程序员' };
const { name, age, job } = user;
console.log(name, age, job);
// 输出结果：张三 25 程序员
```

注意：对象解构用的是花括号 `{}`，而且变量名必须与属性名一致！

#### 重命名（别名）

有时候包裹上的标签（属性名）不方便直接使用，可以给它换个名字：

```javascript
// 把 name 重命名为 userName，job 重命名为 profession
const user = { name: '张三', age: 25, job: '程序员' };
const { name: userName, job: profession } = user;

console.log(userName, profession);
// 输出结果：张三 程序员

// console.log(name);     // 报错！name 未定义
// console.log(job);      // 报错！job 未定义
```

重命名的语法是 `原属性名: 新变量名`，解构后只能用新名字访问。

#### 默认值

和数组解构一样，对象解构也可以设默认值：

```javascript
const user = { name: '张三' };  // 没有 age 和 city
const { name, age = 18, city = '北京' } = user;
console.log(name, age, city);
// 输出结果：张三 18 北京

// 重命名 + 默认值可以一起用
const { name: userName = '匿名' } = {};
console.log(userName);
// 输出结果：匿名
```

#### 嵌套解构

遇到包裹里套包裹的情况（嵌套对象），解构依然能一层层拆开：

```javascript
// ES5：嵌套对象提取
var student = {
  name: '李四',
  score: {
    math: 90,
    english: 85
  }
};
var mathScore = student.score.math;
var englishScore = student.score.english;
console.log(mathScore, englishScore);
// 输出结果：90 85
```

```javascript
// ES6：嵌套解构——一层层"剥开"
const student = {
  name: '李四',
  score: {
    math: 90,
    english: 85
  }
};

// 解构出 name，以及 score 里的 math 和 english
const { name, score: { math, english } } = student;
console.log(name, math, english);
// 输出结果：李四 90 85

// 也可以重命名嵌套属性
const { score: { math: mathScore } } = student;
console.log(mathScore);
// 输出结果：90

// 给嵌套属性设默认值
const product = { title: '手机' };
const { title, detail: { price = 0 } = {} } = product;
console.log(title, price);
// 输出结果：手机 0
// 注意：detail 可能不存在，所以也要给 detail 设默认空对象
```

---

## 3.3 解构的实际应用

### 3.3.1 函数参数解构

在实际开发中，解构最常用的地方之一就是**函数参数**。想象一下，函数的参数就是一个"包裹"，用解构可以直接取出需要的数据。

```javascript
// ES5：函数参数处理
function createUser(options) {
  var name = options.name || '匿名';
  var age = options.age || 18;
  var role = options.role || 'user';
  return name + ' - ' + age + '岁 - ' + role;
}
console.log(createUser({ name: '张三', age: 25 }));
// 输出结果：张三 - 25岁 - user
```

```javascript
// ES6：函数参数解构——在参数位置直接"拆包裹"
function createUser({ name = '匿名', age = 18, role = 'user' }) {
  return `${name} - ${age}岁 - ${role}`;
}
console.log(createUser({ name: '张三', age: 25 }));
// 输出结果：张三 - 25岁 - user

// 嵌套参数解构
function displayStudent({ name, score: { math, english } }) {
  console.log(`${name} 的成绩：数学 ${math}，英语 ${english}`);
}
displayStudent({ name: '李四', score: { math: 90, english: 85 } });
// 输出结果：李四 的成绩：数学 90，英语 85
```

**坑点提醒：** 如果调用函数时不传参数，解构会报错！

```javascript
function greet({ name }) {
  console.log('你好，' + name);
}
greet();  // TypeError: Cannot destructure property 'name' of 'undefined'

// 正确做法：给整个参数设默认值
function greet({ name } = {}) {
  console.log(`你好，${name || '陌生人'}`);
}
greet();           // 输出结果：你好，陌生人
greet({ name: '小明' });  // 输出结果：你好，小明
```

### 3.3.2 交换变量

不用临时变量，一行代码交换两个变量的值——这是解构最"炫技"的用法之一：

```javascript
// ES5：交换变量需要借助临时变量
var a = 1;
var b = 2;
var temp = a;
a = b;
b = temp;
console.log(a, b);
// 输出结果：2 1
```

```javascript
// ES6：解构交换，优雅如丝滑
let a = 1;
let b = 2;
[a, b] = [b, a];  // 右边创建新数组 [2, 1]，再解构到 a 和 b
console.log(a, b);
// 输出结果：2 1
```

这行代码的原理是：先计算右边 `[b, a]` 得到 `[2, 1]`，然后用数组解构把值赋给左边的 `a` 和 `b`。没有临时变量，没有中间商赚差价！

### 3.3.3 提取 API 数据

从后端接口返回的数据中提取信息，是解构最常见的实战场景。

```javascript
// 模拟从 API 获取的数据
const apiResponse = {
  code: 200,
  message: 'success',
  data: {
    user: {
      id: 1001,
      name: '张三',
      email: 'zhangsan@example.com',
      profile: {
        avatar: 'https://example.com/avatar.jpg',
        bio: '热爱编程的前端工程师'
      }
    },
    posts: [
      { id: 1, title: 'ES6入门' },
      { id: 2, title: 'React基础' }
    ]
  }
};

// ES5：层层嵌套的属性提取
var userName = apiResponse.data.user.name;
var avatar = apiResponse.data.user.profile.avatar;
var firstPostTitle = apiResponse.data.posts[0].title;
console.log(userName, avatar, firstPostTitle);
// 输出结果：张三 https://example.com/avatar.jpg ES6入门
```

```javascript
// ES6：解构一步到位，代码清晰如文档
const {
  data: {
    user: {
      name: userName,
      email,
      profile: { avatar, bio }
    },
    posts: [firstPost, secondPost]
  }
} = apiResponse;

console.log(userName, email, avatar, bio);
// 输出结果：张三 zhangsan@example.com https://example.com/avatar.jpg 热爱编程的前端工程师

console.log(firstPost.title, secondPost.title);
// 输出结果：ES6入门 React基础
```

### 3.3.4 配合 for...of 遍历

解构和 `for...of` 循环是天作之合，遍历数组时直接取出需要的值：

```javascript
// 遍历对象数组
const users = [
  { name: '张三', age: 25 },
  { name: '李四', age: 30 },
  { name: '王五', age: 28 }
];

// ES5
for (var i = 0; i < users.length; i++) {
  var name = users[i].name;
  var age = users[i].age;
  console.log(name + '今年' + age + '岁');
}

// ES6：for...of + 解构
for (const { name, age } of users) {
  console.log(`${name}今年${age}岁`);
}
// 输出结果：
// 张三今年25岁
// 李四今年30岁
// 王五今年28岁

// 遍历 Map
const userMap = new Map([
  ['id', 1001],
  ['name', '张三'],
  ['role', 'admin']
]);

for (const [key, value] of userMap) {
  console.log(`${key}: ${value}`);
}
// 输出结果：
// id: 1001
// name: 张三
// role: admin
```

---

## 3.4 本章小结

| 特性 | 核心语法 | 记忆口诀 |
|:---|:---|:---|
| **模板字符串** | `` `内容${变量}` `` | 反引号一包，变量往里塞 |
| **多行字符串** | 直接回车换行 | 告别 `\n`，所见即所得 |
| **表达式插值** | `${a + b}`、 `${fn()}` | 大括号里随便写 |
| **数组解构** | `[a, b, c] = arr` | 按位置拆包裹 |
| **对象解构** | `{a, b} = obj` | 按名字拆包裹 |
| **重命名** | `{a: newA}` | 旧名冒号新名 |
| **默认值** | `[a = 1]`、`{a = 1}` | 等号后面跟保底 |
| **剩余元素** | `[a, ...rest]` | 三个点，收尾巴 |
| **嵌套解构** | `{a: {b}}` | 层层剥开 |
| **函数参数解构** | `fn({a, b})` | 参数位置直接拆 |
| **变量交换** | `[a, b] = [b, a]` | 数组对调，一步完成 |

### 要点回顾

1. **模板字符串**用反引号包裹，变量用 `${}` 插入，支持多行和任意表达式
2. **数组解构**按位置匹配，用逗号跳过元素，`...` 收集剩余元素
3. **对象解构**按属性名匹配，可以用 `:` 重命名，支持嵌套和默认值
4. 解构让代码更短、更清晰，尤其在处理 API 数据和函数参数时威力巨大
5. 记得给可能为空的解构目标设置默认值，避免运行时错误

---

## 3.5 练习题

### 基础题

**1. 模板字符串改写**
将下面的 ES5 字符串拼接改写成模板字符串：
```javascript
var name = '小红';
var count = 5;
var message = '用户' + name + '有' + count + '条未读消息，共' + (count * 2) + '条通知。';
```

**2. 数组解构**
用解构赋值提取以下数组的元素：
```javascript
const coordinates = [120, 30, 100];  // 经度、纬度、海拔
// 要求：经度存到 lng，纬度存到 lat，海拔默认值为 0 存到 altitude
```

**3. 对象解构**
从下面的对象中提取数据：
```javascript
const book = {
  title: 'JavaScript高级程序设计',
  author: { firstName: 'Matt', lastName: 'Frisbie' },
  publisher: { name: '人民邮电出版社', year: 2020 }
};
// 要求：提取 title，提取作者的完整姓名（拼接 firstName 和 lastName），提取出版社名称
```

### 进阶题

**4. 函数参数解构**
编写一个函数 `formatDate`，接收一个对象参数，包含 `year`、`month`、`day` 三个属性（month 和 day 有默认值 1），返回格式为 `YYYY年MM月DD日` 的字符串。

**5. 综合应用**
用解构和模板字符串完成下面的数据展示函数：
```javascript
const students = [
  { name: '张三', scores: { math: 90, english: 80 } },
  { name: '李四', scores: { math: 75, english: 95 } }
];
// 要求输出：
// 张三：数学90分，英语80分，总分170分
// 李四：数学75分，英语95分，总分170分
```

---

> **下一章预告：** 第四章将带你深入探索 ES6 的 **箭头函数** 和 **函数参数增强**（默认参数、剩余参数），让你的函数写法更加简洁优雅。我们不见不散！

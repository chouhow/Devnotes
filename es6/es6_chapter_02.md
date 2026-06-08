# 第二章：箭头函数与函数增强

> 上一章我们见识了`let`和`const`如何让变量声明更加规范。本章将聚焦于**函数**——JavaScript中最核心的"积木"，看看ES6如何让它变得更简洁、更强大、更靠谱。

---

## 2.1 箭头函数（Arrow Function）

### 2.1.1 为什么需要箭头函数？

想象你是一个忙碌的厨师，每次做菜都要先写一套完整的流程："首先，我拿起刀；然后，我切菜；接着……"——这多累人啊！ES5的函数写法就像这套完整流程，而箭头函数就像是厨房里的快捷指令——**快、准、省**。

箭头函数不仅仅是语法糖，它解决了JavaScript中困扰开发者多年的`this`指向问题。但在深入这个话题之前，我们先来看看它长什么样。

### 2.1.2 基本语法形式

箭头函数的语法可以简化成一个公式：

```
(参数) => { 函数体 }
```

让我们从最简单的开始，一步步看它是如何"瘦身"的：

```javascript
// ========== ES5 传统写法 ==========
var add = function(a, b) {
  return a + b;
};

// ========== ES6 箭头函数：完整写法 ==========
const add = (a, b) => {
  return a + b;
};

// ========== ES6 箭头函数：更简写法（单行省略return） ==========
const add = (a, b) => a + b;

console.log(add(2, 3)); // 输出: 5
```

> **注意**：当函数体只有一行表达式时，可以省略花括号`{}`和`return`关键字，表达式的结果会自动返回。

#### 四种简写规则一览

| 场景 | 完整写法 | 简写形式 | 说明 |
|------|----------|----------|------|
| 多参数 | `(a, b) => a + b` | 同上 | 多个参数用括号包裹 |
| 单参数 | `(x) => x * 2` | `x => x * 2` | 只有一个参数时，可省略括号 |
| 无参数 | `() => console.log('hi')` | 同上 | 没有参数，括号不能省 |
| 多行体 | `(a, b) => { return a + b; }` | `(a, b) => { ... }` | 多条语句不能省花括号和return |

```javascript
// ========== 单参数：括号可省略 ==========
// ES5
var double = function(x) {
  return x * 2;
};

// ES6
const double = x => x * 2;  // 简洁！
console.log(double(5)); // 输出: 10

// ========== 无参数：括号不能省 ==========
// ES5
var sayHi = function() {
  return "Hello, ES6!";
};

// ES6
const sayHi = () => "Hello, ES6!";  // 括号必须保留
console.log(sayHi()); // 输出: Hello, ES6!

// ========== 多行函数体：花括号不能省 ==========
// ES5
var calc = function(a, b) {
  var sum = a + b;
  var avg = sum / 2;
  return avg;
};

// ES6
const calc = (a, b) => {
  const sum = a + b;    // 多行需要花括号
  const avg = sum / 2;  // 中间可以有多条语句
  return avg;           // 需要显式 return
};
console.log(calc(10, 20)); // 输出: 15
```

#### 返回对象字面量的坑

```javascript
// ❌ 错误：这样写会被解析为多行语句，不是对象
const getUser = () => { name: "Alice", age: 25 };
// JavaScript 会把 { 当成块级作用域的开始，name 被当成标签

// ✅ 正确：用圆括号包裹对象字面量
const getUser = () => ({ name: "Alice", age: 25 });

console.log(getUser()); // 输出: { name: 'Alice', age: 25 }
```

> **坑点提醒**：箭头函数返回对象时，务必用圆括号`()`包裹，否则花括号会被当成函数体块处理！

---

## 2.2 this 指向：箭头函数的灵魂

### 2.2.1 普通函数的 this 困境

JavaScript的`this`就像个变色龙——它的指向取决于**在哪里调用**，而不是在哪里定义。这让无数开发者掉了不少头发。

```javascript
// ========== ES5：经典的 this 丢失问题 ==========
var person = {
  name: "小明",
  hobbies: ["读书", "游泳", "编程"],
  showHobbies: function() {
    // 这里的 this === person ✅
    console.log(this.name + "的爱好是：");
    
    this.hobbies.forEach(function(hobby) {
      // 问题来了！这里的 this === window（严格模式下是 undefined）❌
      console.log(this.name + "喜欢" + hobby); // undefined喜欢读书
    });
  }
};

person.showHobbies();
// 输出:
// 小明的爱好是：
// undefined喜欢读书
// undefined喜欢游泳
// undefined喜欢编程
```

**为什么会这样？** 因为`forEach`里的普通函数是独立调用的，它有自己的`this`，不再指向`person`。

ES5时代，程序员们发明了各种"歪招"来修复这个问题：

```javascript
// 歪招1：在外面存一个变量
var person = {
  name: "小明",
  hobbies: ["读书", "游泳"],
  showHobbies: function() {
    var that = this;  // 把 this 存起来，江湖人称 "that 大法"
    this.hobbies.forEach(function(hobby) {
      console.log(that.name + "喜欢" + hobby); // ✅ 用 that 代替 this
    });
  }
};

// 歪招2：用 bind 硬绑定
showHobbies: function() {
  this.hobbies.forEach(function(hobby) {
    console.log(this.name + "喜欢" + hobby);
  }.bind(this));  // 把外面的 this 绑进去
}
```

### 2.2.2 箭头函数的 this：借用外层的"寄生虫"

**箭头函数没有自己的`this`！** 它就像寄生虫一样，会**捕获（borrow）外层作用域的`this`**，然后牢牢绑定，永不改变。

用代码说话：

```javascript
// ========== ES6：箭头函数彻底解决 this 问题 ==========
const person = {
  name: "小明",
  hobbies: ["读书", "游泳", "编程"],
  showHobbies() {
    // 这里的 this === person
    console.log(this.name + "的爱好是：");
    
    this.hobbies.forEach(hobby => {
      // 箭头函数 borrow 了外层的 this，所以 this === person ✅
      console.log(this.name + "喜欢" + hobby);
    });
  }
};

person.showHobbies();
// 输出:
// 小明的爱好是：
// 小明喜欢读书
// 小明喜欢游泳
// 小明喜欢编程
```

#### 形象比喻

| 特性 | 普通函数 | 箭头函数 |
|------|----------|----------|
| `this` 来源 | 调用时决定（动态绑定） | 定义时捕获外层`this`（词法绑定） |
| 类比 | 职场墙头草，谁调用就跟谁 | 忠诚的寄生虫，只认出生时的"宿主" |
| 能否被改变 | `call`/`apply`/`bind`可以改变 | 永远无法改变 |

```javascript
// ========== 箭头函数的 this 无法被强行改变 ==========
const team = {
  name: "火箭队",
  showName: () => {
    console.log(this.name);  // this 是外层的，不是 team
  }
};

// 就算用 call/apply/bind，也没用！
team.showName.call({ name: "变脸了" }); // 输出: undefined（或全局的 name）
```

> **核心结论**：箭头函数的`this`在**定义的那一刻就固定了**，之后无论如何调用都无法改变。它永远指向外层（词法）作用域的`this`。

### 2.2.3 词法作用域绑定详解

```javascript
// ========== 层层嵌套，this 始终指向最外层 ==========
const obj = {
  value: 42,
  outer: function() {
    // 普通函数：this === obj
    console.log("outer this:", this.value); // 42
    
    const inner1 = () => {
      // 箭头函数：borrow 外层 outer 的 this → obj
      console.log("inner1 this:", this.value); // 42
      
      const inner2 = () => {
        // 箭头函数：继续 borrow 外层 inner1 的 this → 还是 obj
        console.log("inner2 this:", this.value); // 42
      };
      inner2();
    };
    inner1();
  }
};

obj.outer();
```

> 箭头函数的`this`不取决于它在哪里被调用，而取决于它在哪里被**定义**。这就是**词法作用域绑定**的含义。

---

## 2.3 箭头函数的适用场景

### 2.3.1 数组方法的回调函数

这是箭头函数最经典、最常用的地方：

```javascript
const numbers = [1, 2, 3, 4, 5];

// ========== ES5：传统写法，又臭又长 ==========
var doubled = numbers.map(function(n) {
  return n * 2;
});
var evens = numbers.filter(function(n) {
  return n % 2 === 0;
});
var sum = numbers.reduce(function(acc, n) {
  return acc + n;
}, 0);

// ========== ES6：箭头函数，清爽简洁 ==========
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
const sum = numbers.reduce((acc, n) => acc + n, 0);

console.log(doubled); // [2, 4, 6, 8, 10]
console.log(evens);   // [2, 4]
console.log(sum);     // 15
```

### 2.3.2 定时器和事件回调

```javascript
// ========== ES5：setTimeout 里的 this 丢失 ==========
var Timer = function() {
  this.seconds = 0;
  setInterval(function() {
    this.seconds++;  // ❌ this 指向 window，不是 Timer 实例
    console.log(this.seconds);
  }, 1000);
};

// ========== ES6：箭头函数自动捕获正确的 this ==========
class Timer {
  constructor() {
    this.seconds = 0;
    setInterval(() => {
      this.seconds++;  // ✅ this 指向 Timer 实例
      console.log(this.seconds); // 1, 2, 3, 4...
    }, 1000);
  }
}
```

### 2.3.3 Promise 链式调用

```javascript
// ========== ES5：Promise 回调里 this 容易丢失 ==========
fetchUserData(userId)
  .then(function(user) {
    return this.processUser(user); // ❌ this 可能不对
  }.bind(this))  // 不得不 bind
  .then(function(processed) {
    console.log(processed);
  });

// ========== ES6：箭头函数省心省力 ==========
fetchUserData(userId)
  .then(user => this.processUser(user))  // ✅ this 自动正确
  .then(processed => console.log(processed));
```

---

## 2.4 箭头函数不适用场景（避坑指南）

箭头函数虽然好，但不是万能的。以下场景**千万别用**箭头函数！

### 2.4.1 构造函数

箭头函数没有自己的`this`，所以不能用作构造函数，也不能使用`new`调用。

```javascript
// ❌ 错误：箭头函数不能当构造函数
const Person = (name) => {
  this.name = name;  // 这里不会报错，但 this 不是新创建的实例
};

const p = new Person("Alice"); // TypeError: Person is not a constructor

// ✅ 正确：用 class 或普通函数
class Person {
  constructor(name) {
    this.name = name;  // ✅ this 指向新创建的实例
  }
}
const p = new Person("Alice");
console.log(p.name); // Alice
```

> **原因**：构造函数需要`this`指向新创建的实例对象，但箭头函数的`this`被固定绑定到外层，无法满足需求。

### 2.4.2 对象方法（需要动态 this 的情况）

```javascript
// ❌ 错误：箭头函数作为对象方法
cat = {
  name: "咪咪",
  sayName: () => {
    // this 指向外层（window/global），不是 cat
    console.log(this.name);
  }
};
cat.sayName(); // undefined（或全局的 name）

// ✅ 正确：普通函数或方法简写
cat = {
  name: "咪咪",
  sayName() {  // ES6 方法简写
    // this 指向调用者 cat
    console.log(this.name);
  }
};
cat.sayName(); // 咪咪
```

### 2.4.3 需要 arguments 对象的场景

箭头函数没有自己的`arguments`对象。

```javascript
// ❌ 错误：箭头函数没有自己的 arguments
const showArgs = () => {
  console.log(arguments);  // 指向外层 arguments，不是你想要的
};
showArgs(1, 2, 3);

// ✅ 正确：普通函数有自己的 arguments
function showArgs() {
  console.log(arguments);  // [1, 2, 3]
}
showArgs(1, 2, 3);

// ✅ 或者用剩余参数（下面会讲）
const showArgs = (...args) => {
  console.log(args);  // [1, 2, 3]
};
showArgs(1, 2, 3);
```

### 2.4.4 需要动态 this 的 DOM 事件处理

```javascript
// ❌ 错误：this 不指向按钮
button.addEventListener("click", () => {
  this.classList.add("active"); // this 指向外层，不是 button
});

// ✅ 正确：普通函数的 this 指向触发事件的元素
button.addEventListener("click", function() {
  this.classList.add("active"); // ✅ this === button
});
```

### 适用 vs 不适用场景总结

| 场景 | 是否适合箭头函数 | 原因 |
|------|------------------|------|
| 数组方法回调（map/filter/reduce） | ✅ 适合 | 简洁，无 this 困扰 |
| 定时器回调 | ✅ 适合 | 自动捕获正确 this |
| Promise 链 | ✅ 适合 | 简洁，无需 bind |
| 简单工具函数 | ✅ 适合 | 一行搞定 |
| **构造函数** | ❌ 不适合 | 不能作为构造器使用 |
| **对象方法** | ❌ 不适合 | this 不指向对象本身 |
| **DOM 事件处理** | ❌ 不适合 | 需要 this 指向 DOM 元素 |
| **需要 arguments** | ❌ 不适合 | 没有自己的 arguments |
| **需要 call/apply/bind** | ❌ 不适合 | this 不可被改变 |

---

## 2.5 默认参数（Default Parameters）

### 2.5.1 为什么要默认参数？

想象你去奶茶店点单，不说糖度，店员应该给你**默认糖度**（比如七分糖），而不是给你一杯"undefined糖"的怪东西。ES5的函数参数就是这样——不传就是`undefined`，经常出 bug。

```javascript
// ========== ES5：手动处理默认值的笨拙方式 ==========
function greet(name, greeting) {
  // 如果不传参数，name 和 greeting 都是 undefined
  name = name || "陌生人";        // 用 || 来设置默认值
  greeting = greeting || "你好";  // 但 0、""、false 也会被误判！
  return greeting + "，" + name + "！";
}

console.log(greet());          // "你好，陌生人！" ✅
console.log(greet("", ""));    // "你好，陌生人！" ❌ 用户想传空字符串却被覆盖

// 更安全的写法，但啰嗦
function greet(name, greeting) {
  name = (name !== undefined) ? name : "陌生人";
  greeting = (greeting !== undefined) ? greeting : "你好";
  return greeting + "，" + name + "！";
}
```

### 2.5.2 ES6 默认参数语法

```javascript
// ========== ES6：直接在参数列表里写默认值 ==========
function greet(name = "陌生人", greeting = "你好") {
  return `${greeting}，${name}！`;
}

console.log(greet());                 // "你好，陌生人！"
console.log(greet("小明"));           // "你好，小明！"
console.log(greet("小明", "早上好"));  // "早上好，小明！"
console.log(greet("", ""));           // "，！" ✅ 空字符串不会被覆盖
```

> **语法**：在参数名后面用 `= 值` 的形式指定默认值。当传入的参数是`undefined`时，默认值生效。

### 2.5.3 默认值可以是表达式

```javascript
// 默认值可以是函数调用的结果
function getDefaultId() {
  return Math.random().toString(36).substr(2, 9);
}

function createUser(name, id = getDefaultId()) {
  return { name, id };
}

console.log(createUser("Alice"));
// { name: 'Alice', id: 'x7k3m9p2q' } 自动生成唯一ID

// 默认值甚至可以引用前面的参数
function createRect(width, height = width) {
  // 如果不传 height，默认等于 width，即正方形
  return { width, height };
}

console.log(createRect(100));     // { width: 100, height: 100 }
console.log(createRect(100, 50)); // { width: 100, height: 50 }
```

### 2.5.4 默认参数的求值时机

```javascript
// 默认值在函数调用时求值，不是定义时
let defaultName = "默认名字";

function show(name = defaultName) {
  return name;
}

console.log(show()); // "默认名字"

defaultName = "新名字";
console.log(show()); // "新名字" ← 默认值是动态求值的

// 不传参 vs 传 undefined 都会触发默认值
function test(a = "默认值") {
  return a;
}
console.log(test());           // "默认值"
console.log(test(undefined));  // "默认值"
console.log(test(null));       // null ← null 不会触发默认值！
```

> **坑点提醒**：只有`undefined`会触发默认值，`null`不会！因为`null`是一个明确的值。

### 2.5.5 箭头函数也能用默认参数

```javascript
const multiply = (a, b = 1) => a * b;

console.log(multiply(5));    // 5 (5 * 1)
console.log(multiply(5, 2)); // 10
console.log(multiply(5, 0)); // 0 ← 0 不会触发默认值

// 实用例子：延迟操作
const delay = (ms = 1000) => new Promise(resolve => setTimeout(resolve, ms));
delay().then(() => console.log("1秒后执行"));       // 默认延迟1秒
delay(500).then(() => console.log("0.5秒后执行"));  // 自定义延迟
```

---

## 2.6 剩余参数（Rest Parameters）：...args

### 2.6.1 剩余参数是什么？

想象你去吃自助餐，盘子里已经放了固定几样菜（命名参数），后面还可以**无限堆叠**（剩余参数）。`...args`就是帮你把"后面所有东西"收集到一个数组里。

```javascript
// ========== ES5：用 arguments 收集参数 ==========
function sum() {
  // arguments 是类数组对象，不是真正的数组
  var total = 0;
  for (var i = 0; i < arguments.length; i++) {
    total += arguments[i];  // 能用，但没有数组方法
  }
  return total;
}

console.log(sum(1, 2, 3, 4, 5)); // 15

// 如果想用数组方法？先转换！
function sumES5() {
  var args = Array.prototype.slice.call(arguments); // 😫 好丑
  return args.reduce(function(a, b) { return a + b; }, 0);
}
```

### 2.6.2 ES6 剩余参数语法

```javascript
// ========== ES6：剩余参数，真正的数组 ==========
function sum(...numbers) {
  // numbers 是真正的数组，可以直接用数组方法
  return numbers.reduce((a, b) => a + b, 0);
}

console.log(sum(1, 2, 3));     // 6
console.log(sum(1, 2, 3, 4, 5, 6, 7)); // 28
console.log(sum());            // 0
```

> **语法**：在最后一个参数前加`...`，它会收集**所有剩余参数**到一个真正的数组中。

### 2.6.3 剩余参数配合命名参数

```javascript
// 前面是命名参数，...others 收集剩余的
function introduce(firstName, lastName, ...hobbies) {
  console.log(`我叫${lastName}${firstName}`);
  if (hobbies.length > 0) {
    console.log(`我的爱好有：${hobbies.join("、")}`);
  }
}

introduce("明", "王", "编程", "游泳", "阅读");
// 输出:
// 我叫王明
// 我的爱好有：编程、游泳、阅读

introduce("Alice", "Smith");
// 输出:
// 我叫SmithAlice
// hobbies 是空数组 []
```

### 2.6.4 箭头函数与剩余参数

```javascript
// 箭头函数没有自己的 arguments，所以剩余参数特别重要！
const logAll = (...args) => {
  // args 是真正的数组，可以用 forEach、map 等
  args.forEach((item, index) => {
    console.log(`${index}: ${item}`);
  });
};

logAll("苹果", "香蕉", "橙子");
// 输出:
// 0: 苹果
// 1: 香蕉
// 2: 橙子
```

### 2.6.5 剩余参数 vs arguments 对比

| 特性 | `arguments`（ES5） | `...rest`（ES6） |
|------|--------------------|--------------------|
| 类型 | 类数组对象 | 真正的数组 |
| 能否用数组方法 | 不能直接用（需转换） | 可以直接用 |
| 箭头函数中 | 借用外层的 arguments | ✅ 有自己的 rest |
| 包含已命名参数 | ✅ 包含所有参数 | 只包含**剩余**参数 |
| 可读性 | 低（不知道哪些参数是干啥的） | 高（命名 + 剩余分离） |

```javascript
// arguments 包含所有参数，包括已命名的
function demo(a, b) {
  console.log(arguments); // [1, 2, 3, 4] - 全部
  console.log(a, b);      // 1, 2
}
demo(1, 2, 3, 4);

// rest 只包含剩余参数
function demo2(a, b, ...rest) {
  console.log(rest); // [3, 4] - 只有剩余的
  console.log(a, b); // 1, 2
}
demo2(1, 2, 3, 4);
```

### 2.6.6 实用技巧：解构 + 剩余参数

```javascript
// 解构前几个元素，剩余归为一个数组
const [first, second, ...rest] = [10, 20, 30, 40, 50];
console.log(first);  // 10
console.log(second); // 20
console.log(rest);   // [30, 40, 50]

// 函数参数中同样适用
function processHeader(first, second, ...data) {
  console.log("Header1:", first);
  console.log("Header2:", second);
  console.log("Data:", data);
}
processHeader("姓名", "年龄", "小明", "25", "北京", "工程师");
// Header1: 姓名
// Header2: 年龄
// Data: ['小明', '25', '北京', '工程师']
```

> **坑点提醒**：`...rest`必须是最后一个参数，后面不能再有其他参数！

---

## 2.7 展开运算符（Spread Operator）：... 的另一种用法

### 2.7.1 展开运算符是什么？

剩余参数和展开运算符长得一样（都是`...`），但用法正好相反：

- **剩余参数**：把多个值 → 收集成一个数组
- **展开运算符**：把一个数组 → 展开成多个值

就像**拉链**和**拉开拉链**的关系——一个收拢，一个展开。

### 2.7.2 数组展开

```javascript
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];

// ========== ES5：拼接数组 ==========
var combined = arr1.concat(arr2);  // [1, 2, 3, 4, 5, 6]
var withExtra = [0].concat(arr1, arr2, [7]);  // [0, 1, 2, 3, 4, 5, 6, 7]

// ========== ES6：用展开运算符，直观优雅 ==========
const combined = [...arr1, ...arr2];           // [1, 2, 3, 4, 5, 6]
const withExtra = [0, ...arr1, ...arr2, 7];    // [0, 1, 2, 3, 4, 5, 6, 7]

// 还可以在中间插入
const inserted = [...arr1, "插入", ...arr2];   // [1, 2, 3, '插入', 4, 5, 6]

// 复制数组（浅拷贝）
const copy = [...arr1];
console.log(copy);      // [1, 2, 3]
console.log(copy === arr1); // false ✅ 新的数组
```

### 2.7.3 展开运算符用于函数调用

```javascript
const numbers = [10, 5, 30, 2, 100];

// ========== ES5：用 apply 来传数组参数 ==========
var max = Math.max.apply(null, numbers);  // 100
// apply 语法怪异，第一个参数是 this 绑定

// ========== ES6：用展开运算符，直接展开数组 ==========
const max = Math.max(...numbers);   // 100
const min = Math.min(...numbers);   // 2

// 相当于 Math.max(10, 5, 30, 2, 100)

// 混合使用：普通参数 + 展开的数组
function greet(greeting, ...names) {
  return `${greeting}，${names.join("和")}！`;
}
const friends = ["小明", "小红", "小刚"];
console.log(greet("大家好", ...friends)); // "大家好，小明和小红和小刚！"
```

### 2.7.4 对象展开（ES2018）

对象展开是ES2018的特性，但已经被广泛使用：

```javascript
const person = { name: "小明", age: 25 };
const address = { city: "北京", country: "中国" };

// ========== ES5：合并对象 ==========
var merged = Object.assign({}, person, address);
// { name: "小明", age: 25, city: "北京", country: "中国" }

// ========== ES6+：用展开运算符 ==========
const merged = { ...person, ...address };
console.log(merged);
// { name: '小明', age: 25, city: '北京', country: '中国' }

// 还可以添加新属性或覆盖
const updated = { ...person, age: 26, job: "工程师" };
console.log(updated);
// { name: '小明', age: 26, job: '工程师' }
```

### 2.7.5 展开运算符的实用技巧

```javascript
// ========== 技巧1：数组去重（配合 Set） ==========
const nums = [1, 2, 2, 3, 3, 3, 4];
const unique = [...new Set(nums)];
console.log(unique); // [1, 2, 3, 4]

// ========== 技巧2：字符串转字符数组 ==========
const chars = [..."Hello"];
console.log(chars); // ['H', 'e', 'l', 'l', 'o']

// ========== 技巧3：类数组转真数组 ==========
function demo() {
  const args = [...arguments]; // 或直接用剩余参数
  return args.map(x => x * 2);
}
console.log(demo(1, 2, 3)); // [2, 4, 6]

// ========== 技巧4：对象浅拷贝 + 修改 ==========
const user = { name: "Alice", age: 25, hobbies: ["读书"] };
const newUser = { ...user, age: 26 };  // 修改 age

// 注意：这是浅拷贝！
newUser.hobbies.push("游泳");
console.log(user.hobbies);     // ['读书', '游泳'] ← 原对象也被改了！

// 深拷贝需要用：
const deepClone = JSON.parse(JSON.stringify(user));

// ========== 技巧5：条件展开 ==========
const showExtra = true;
const config = {
  name: "基本配置",
  ...(showExtra ? { debug: true, logLevel: "verbose" } : {})
};
console.log(config);
// { name: '基本配置', debug: true, logLevel: 'verbose' }
```

### 2.7.6 展开运算符 vs 剩余参数对比

虽然长得一样（都是`...`），但用法完全不同：

| 场景 | 角色 | 作用 | 示例 |
|------|------|------|------|
| 函数**参数**定义中 | 剩余参数 | 收拢参数为数组 | `fn(a, ...rest)` |
| 函数**调用**中 | 展开运算符 | 展开数组为参数 | `fn(...arr)` |
| 数组**字面量**中 | 展开运算符 | 展开数组元素 | `[...arr1, ...arr2]` |
| 解构赋值中 | 剩余参数 | 收集剩余元素 | `[a, ...rest] = arr` |

```javascript
// 总结示例：... 在不同位置的两种含义

// 位置1：函数参数 → 剩余参数（收拢）
function collect(first, ...rest) {
  // rest = [2, 3, 4, 5]
  return rest;
}

// 位置2：函数调用 → 展开运算符（展开）
const arr = [1, 2, 3];
collect(...arr);  // 相当于 collect(1, 2, 3)

// 位置3：数组字面量 → 展开运算符
const newArr = [...arr, 4, 5];  // [1, 2, 3, 4, 5]

// 位置4：解构 → 剩余参数
const [a, ...others] = arr;  // a=1, others=[2, 3]
```

---

## 2.8 本章综合实战

### 实战1：一个灵活的日志工具

```javascript
/**
 * 灵活的日志工具
 * - 默认参数：设置默认级别
 * - 剩余参数：支持多个参数
 * - 展开运算符：格式化输出
 */
const logger = {
  // 默认日志级别为 'info'
  log(level = "info", ...messages) {
    const timestamp = new Date().toLocaleTimeString();
    const prefixes = {
      info: "ℹ️",
      warn: "⚠️",
      error: "❌",
      success: "✅"
    };
    const prefix = prefixes[level] || "📝";
    console.log(`[${timestamp}] ${prefix}`, ...messages);
  },
  
  // 快捷方法
  info: (...msgs) => logger.log("info", ...msgs),
  warn: (...msgs) => logger.log("warn", ...msgs),
  error: (...msgs) => logger.log("error", ...msgs)
};

logger.info("系统启动", "版本: 1.0.0");
// 输出: [10:30:25] ℹ️ 系统启动 版本: 1.0.0

logger.error("连接失败", { code: 500 });
// 输出: [10:30:25] ❌ 连接失败 { code: 500 }
```

### 实战2：配置合并工具

```javascript
/**
 * 合并用户配置和默认配置
 * 运用：默认参数 + 对象展开 + 箭头函数
 */
const defaultConfig = {
  timeout: 5000,
  retries: 3,
  headers: {
    "Content-Type": "application/json"
  }
};

const mergeConfig = (userConfig = {}) => ({
  ...defaultConfig,
  ...userConfig,
  // headers 需要深度合并
  headers: {
    ...defaultConfig.headers,
    ...userConfig.headers
  }
});

// 只覆盖 timeout
console.log(mergeConfig({ timeout: 10000 }));
// { timeout: 10000, retries: 3, headers: { 'Content-Type': 'application/json' } }

// 添加自定义 header
console.log(mergeConfig({ headers: { Authorization: "Bearer xxx" } }));
// { timeout: 5000, retries: 3, headers: { 'Content-Type': 'application/json', Authorization: 'Bearer xxx' } }
```

### 实战3：管道函数组合

```javascript
/**
 * 将多个函数组合成管道
 * 运用：箭头函数 + 剩余参数 + 展开运算符
 */
const pipe = (...functions) => input =>
  functions.reduce((value, fn) => fn(value), input);

// 定义一些简单的纯函数
const double = x => x * 2;
const addOne = x => x + 1;
const toString = x => `结果: ${x}`;

// 组合管道
const process = pipe(double, addOne, toString);
console.log(process(5)); // "结果: 11" ((5 * 2) + 1 = 11)

// 另一个管道
const formatPrice = pipe(
  x => x * 0.8,        // 8折
  x => Math.round(x),  // 四舍五入
  x => `¥${x}`         // 格式化
);
console.log(formatPrice(99.9)); // "¥80"
```

---

## 2.9 本章小结

### 核心知识点回顾

```
┌─────────────────────────────────────────────────────────────┐
│                      本章知识地图                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  箭头函数 () => {}                                          │
│  ├── 语法简写：单参数省括号，单行省return和花括号           │
│  ├── this 特性：没有自己的this，借用外层词法this            │
│  ├── ✅ 适合：回调函数、数组方法、定时器、Promise链         │
│  └── ❌ 不适合：构造函数、对象方法、DOM事件、需要arguments  │
│                                                             │
│  默认参数 (param = default)                                 │
│  ├── 解决 undefined 问题                                    │
│  ├── 默认值可以是表达式                                     │
│  └── null 不会触发默认值                                    │
│                                                             │
│  剩余参数 ...rest                                           │
│  ├── 收集剩余参数为真正数组                                 │
│  ├── 替代不可靠的 arguments                                 │
│  └── 必须是最后一个参数                                     │
│                                                             │
│  展开运算符 ...                                             │
│  ├── 数组展开：[...arr1, ...arr2]                           │
│  ├── 对象展开：{...obj1, ...obj2}                           │
│  ├── 函数调用：fn(...arr)                                   │
│  └── 与剩余参数是反向操作                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 记忆口诀

> **箭头函数没有 this，借用外层不客气。**
> **默认参数防 undefined，写在等号右边行。**
> **剩余参数...rest收，展开运算符...散开。**
> **构造函数别用箭头，对象方法也同理。**

### 下章预告

在第三章中，我们将深入探索**解构赋值**——一种像" unpacking 拆快递包裹"一样从数组和对象中提取数据的优雅语法。它能让你用一行代码完成过去需要多行的赋值操作，配合本章的箭头函数和剩余参数，代码将变得更加行云流水。

---

> **练习建议**：打开你的编辑器，把本章的每个示例都敲一遍，特别是`this`指向的几个对比示例。箭头函数的`this`规则看似复杂，但只要记住"**箭头函数没有自己的this**"这句话，你就已经掌握了90%。

# 第四章：数组与对象的扩展

> 想象你有一个万能工具箱，ES6 不仅给你塞满了新工具，还给旧工具升级了炫酷的新功能。这一章，我们来好好盘一盘数组和对象这两大"数据巨头"的新变化。

---

## 一、数组的新方法

ES6 为数组家族引入了一票实用的新方法，它们就像是给旧工具箱加了电动螺丝刀——以前能做的事现在更简单，以前很麻烦的事现在几行搞定。

### 1.1 find() —— 找到第一个匹配的元素

#### 为什么需要它？

以前要从数组里找一个符合条件的元素，通常需要写循环遍历。`find()` 方法的出现，让查找变得优雅又直观。

#### 语法

```javascript
array.find(callback(element[, index[, array]])[, thisArg])
```

- `callback`：每个元素执行的测试函数，返回 `true` 则返回该元素
- `thisArg`（可选）：执行 callback 时的 `this` 值

#### ES5 vs ES6 对比

```javascript
// ========== ES5 写法：用循环手动查找 ==========
var users = [
  { id: 1, name: '张三', age: 25 },
  { id: 2, name: '李四', age: 30 },
  { id: 3, name: '王五', age: 25 }
];

var found = null;
for (var i = 0; i < users.length; i++) {
  if (users[i].age === 25) {
    found = users[i];        // 找到第一个就停
    break;                   // 别忘了 break，否则会继续找
  }
}
console.log(found);          // { id: 1, name: '张三', age: 25 }

// ========== ES6 写法：find() 一步到位 ==========
const users = [
  { id: 1, name: '张三', age: 25 },
  { id: 2, name: '李四', age: 30 },
  { id: 3, name: '王五', age: 25 }
];

const found = users.find(user => user.age === 25);
//           ↑ find() 返回第一个满足条件的元素本身
console.log(found);          // { id: 1, name: '张三', age: 25 }

// 找不到时返回 undefined
const notFound = users.find(user => user.age === 99);
console.log(notFound);       // undefined
```

#### 实际应用场景：根据 ID 查找数据

```javascript
// 从服务器返回的用户列表中，找到当前登录用户
const currentUserId = 2;
const currentUser = users.find(user => user.id === currentUserId);
console.log(currentUser);    // { id: 2, name: '李四', age: 30 }
```

---

### 1.2 findIndex() —— 找到第一个匹配的位置

`findIndex()` 和 `find()` 是亲兄弟，区别在于一个返回**元素本身**，一个返回**元素的索引**。

```javascript
// ========== ES5 写法 ==========
var index = -1;  // 初始值设为 -1，表示"未找到"
for (var i = 0; i < users.length; i++) {
  if (users[i].age === 25) {
    index = i;
    break;
  }
}
console.log(index);          // 0（第一个匹配元素的位置）

// ========== ES6 写法 ==========
const index = users.findIndex(user => user.age === 25);
//              ↑ findIndex() 返回第一个满足条件的索引
console.log(index);          // 0

// 找不到返回 -1（和 indexOf 保持一致）
const notFoundIndex = users.findIndex(user => user.age === 99);
console.log(notFoundIndex);  // -1
```

> **坑点提醒**：`findIndex()` 和 `indexOf()` 的区别在于，`indexOf()` 只能用严格相等（`===`）判断，而 `findIndex()` 可以用任意复杂的条件。

```javascript
// indexOf 做不到的事，findIndex 可以轻松做到
const arr = [5, 12, 8, 130, 44];

// indexOf：只能找精确值
arr.indexOf(x => x > 10);       // -1 ❌ 传入函数没用

// findIndex：可以用条件判断
arr.findIndex(x => x > 10);     // 1  ✅ 返回 12 的索引
```

---

### 1.3 includes() —— 数组中是否包含某个值

`includes()` 方法用来判断数组是否包含某个值，返回布尔类型。它是 `indexOf()` 的优雅替代。

#### ES5 vs ES6 对比

```javascript
var arr = [1, 3, 5, 7, NaN];

// ========== ES5 写法：用 indexOf 判断（坑多多）==========
// 问题 1：可读性差，需要 !== -1
var hasThree = arr.indexOf(3) !== -1;
console.log(hasThree);       // true

// 问题 2：无法判断 NaN
var hasNaN = arr.indexOf(NaN) !== -1;
console.log(hasNaN);         // false ❌ 明明有 NaN，却返回 false！

// 问题 3：语义不清晰，新手常忘 !== -1
var hasTen = arr.indexOf(10);
if (hasTen) {                // ❌ 坑！indexOf 返回 -1 是"真值"（非零）
  console.log('有 10');      //    实际上会走进这个分支！
}

// ========== ES6 写法：includes() 语义清晰 ==========
const arr = [1, 3, 5, 7, NaN];

console.log(arr.includes(3));      // true  ✅ 一目了然
console.log(arr.includes(NaN));    // true  ✅ 正确判断 NaN！
console.log(arr.includes(10));     // false ✅ 不存在就是 false
```

#### includes() 的两个参数

```javascript
const arr = ['a', 'b', 'c', 'd', 'e'];

// 从指定索引位置开始查找
console.log(arr.includes('c', 3));   // false，从索引 3 开始找，跳过 'c'
console.log(arr.includes('c', 2));   // true，从索引 2 开始找，包含 'c'
```

#### indexOf vs includes 对比表

| 特性 | `indexOf()` | `includes()` |
|------|-----------|------------|
| 返回值 | 索引数字（-1 表示不存在） | 布尔值 |
| 查找 NaN | ❌ 无法查找（NaN !== NaN） | ✅ 可以正确查找 |
| 语义 | 需要 `!== -1` 判断 | 直接返回 true/false |
| 可读性 | 一般 | 极佳 |
| 适用场景 | 需要索引位置时 | 只需判断是否存在时 |

---

### 1.4 Array.from() —— 类数组对象的"变身术"

`Array.from()` 是 ES6 中最实用的数组工具之一，它可以把**类数组对象**和**可迭代对象**转换成真正的数组。

#### 什么是类数组对象？

类数组对象（Array-like Object）长得像数组，有 `length` 属性和索引，但没有数组的方法（如 `push`、`forEach` 等）。最典型的例子是函数内部的 `arguments` 对象和 DOM 返回的 `NodeList`。

```javascript
// 类数组对象示例
var arrayLike = {
  0: '苹果',
  1: '香蕉',
  2: '橘子',
  length: 3
  // ↑ 注意：有 length 属性，但没有数组方法
};

// 不能用数组方法！
// arrayLike.forEach(...)  // ❌ TypeError: arrayLike.forEach is not a function
// arrayLike.map(...)      // ❌ 同样报错
```

#### ES5 vs ES6 对比

```javascript
// ========== ES5 写法：把 arguments 转成数组 ==========
function oldStyle() {
  // 方法一：Array.prototype.slice
  var args = Array.prototype.slice.call(arguments);
  //                    ↑ 借 slice 方法，用 call 把 this 指向 arguments

  // 方法二：更短的写法
  var args2 = [].slice.call(arguments);

  return args.map(function(x) { return x * 2; });
}
console.log(oldStyle(1, 2, 3));   // [2, 4, 6]


// ========== ES6 写法：Array.from() 语义明确 ==========
function newStyle() {
  // Array.from() 清晰表达"从一个类数组创建数组"
  const args = Array.from(arguments);

  return args.map(x => x * 2);
}
console.log(newStyle(1, 2, 3));   // [2, 4, 6]

// 当然，更好的做法是用剩余参数（第三章学过）
function bestStyle(...args) {
  return args.map(x => x * 2);
}
```

#### Array.from() 的典型应用场景

```javascript
// 场景 1：DOM 操作，将 NodeList 转为数组
const nodeList = document.querySelectorAll('div');
// nodeList 是 NodeList，不是真正的数组，没有 map/filter 等方法

// ES5
var divArray = [].slice.call(nodeList);
divArray.forEach(function(div) { div.style.color = 'red'; });

// ES6
const divArray = Array.from(nodeList);
divArray.forEach(div => div.style.color = 'red');


// 场景 2：转换字符串为字符数组
const chars = Array.from('Hello');
console.log(chars);          // ['H', 'e', 'l', 'l', 'o']

// 场景 3：配合 Set 去重
const nums = [1, 2, 2, 3, 3, 3];
const unique = Array.from(new Set(nums));
console.log(unique);         // [1, 2, 3]


// 场景 4：第二个参数是映射函数（相当于 map）
const numbers = Array.from([1, 2, 3], x => x * 10);
//              ↑ 在转换的同时对每个元素做处理
console.log(numbers);        // [10, 20, 30]

// 上面的代码等价于
const numbers2 = Array.from([1, 2, 3]).map(x => x * 10);
```

#### 生成有序数组的小技巧

```javascript
// 快速生成 0~4 的数组
const range = Array.from({ length: 5 }, (_, i) => i);
//                       ↑ 类数组对象 {length: 5}
//                               ↑ _ 表示我们不用的第一个参数（元素值）
//                                 i 是索引，从 0 开始
console.log(range);          // [0, 1, 2, 3, 4]

// 生成 1~5
const range2 = Array.from({ length: 5 }, (_, i) => i + 1);
console.log(range2);         // [1, 2, 3, 4, 5]
```

---

### 1.5 Array.of() —— 创建数组的新姿势

`Array.of()` 用于创建一个新的数组实例，它解决了 `Array()` 构造函数的一个历史遗留问题。

#### Array() 的坑

```javascript
// ========== ES5 的坑：Array() 构造函数的行为不统一 ==========
var arr1 = new Array(3);        // 传一个数字？
console.log(arr1);              // [empty × 3]  ← 创建了一个长度为 3 的空数组！
console.log(arr1.length);       // 3
console.log(arr1[0]);           // undefined

var arr2 = new Array(3, 4, 5);  // 传多个参数？
console.log(arr2);              // [3, 4, 5]    ← 这才是正常创建数组！

// 你看，同样的 Array()，传 1 个参数和传多个参数，行为完全不同！
// 这是因为历史原因造成的歧义
```

#### Array.of() 的一致性

```javascript
// ========== ES6：Array.of() 永远把你传的参数当作元素 ==========
const arr1 = Array.of(3);
console.log(arr1);              // [3]        ← 就是包含 3 的数组

const arr2 = Array.of(3, 4, 5);
console.log(arr2);              // [3, 4, 5]  ← 和上面行为一致

const arr3 = Array.of();        // 不传参数
console.log(arr3);              // []         ← 空数组

const arr4 = Array.of('hello');
console.log(arr4);              // ['hello']
```

> **实际建议**：日常开发中，直接用数组字面量 `[]` 就好，`Array.of()` 主要用于函数式编程中需要把 Array 作为参数传递的场景。

---

### 1.6 fill() / copyWithin()（简要了解）

这两个方法用得相对较少，但了解它们可以在特定场景下提高效率。

#### fill() —— 填充数组

```javascript
// ========== ES5：手动循环填充 ==========
var arr = new Array(5);
for (var i = 0; i < arr.length; i++) {
  arr[i] = 0;
}
console.log(arr);            // [0, 0, 0, 0, 0]

// ========== ES6：fill() 一键填充 ==========
const arr = new Array(5).fill(0);
console.log(arr);            // [0, 0, 0, 0, 0]

// 指定填充范围 [start, end)
const arr2 = [1, 2, 3, 4, 5];
arr2.fill('x', 1, 4);        // 从索引 1 填充到 3（不包含 4）
console.log(arr2);           // [1, 'x', 'x', 'x', 5]
```

#### copyWithin() —— 数组内部复制

```javascript
// copyWithin(target, start, end)
// 把数组中 [start, end) 的部分复制到 target 位置

const arr = [1, 2, 3, 4, 5];
arr.copyWithin(0, 3, 5);
// ↑ 把索引 [3,5) 的元素（即 4, 5）复制到索引 0 的位置

console.log(arr);            // [4, 5, 3, 4, 5]
// 解释：[4, 5] 被复制到了开头，覆盖了原来的 [1, 2]
```

> **小贴士**：`fill()` 在初始化数组时很有用，`copyWithin()` 在需要高性能内部数据移动时使用（如游戏开发中的环形缓冲区）。

---

### 📋 数组新方法汇总表

| 方法 | 作用 | 返回值 | ES5 替代方案 |
|------|------|--------|-------------|
| `find(fn)` | 查找第一个符合条件的元素 | 元素本身 / `undefined` | `for` 循环 + `break` |
| `findIndex(fn)` | 查找第一个符合条件的索引 | 索引 / `-1` | `for` 循环 + `break` |
| `includes(val)` | 判断是否包含某值 | `true` / `false` | `indexOf() !== -1` |
| `Array.from(obj)` | 类数组/可迭代对象 → 数组 | 新数组 | `[].slice.call(obj)` |
| `Array.of(...args)` | 用参数创建数组（无歧义） | 新数组 | `[a, b, c]` 字面量 |
| `fill(val, s, e)` | 用固定值填充数组区间 | 修改后的原数组 | `for` 循环赋值 |
| `copyWithin(t, s, e)` | 数组内部复制片段 | 修改后的原数组 | 手动 splice + 拼接 |

---

## 二、对象的简洁表示法

ES6 让对象的写法变得更加简洁，减少了很多不必要的重复。

### 2.1 属性简写（Property Shorthand）

当对象的属性名和变量名相同时，可以只写属性名。

#### ES5 vs ES6 对比

```javascript
// ========== ES5 写法：属性名和变量名要重复写 ==========
var name = '张三';
var age = 25;
var job = '前端工程师';

var person = {
  name: name,     // ← "name" 写了两遍
  age: age,       // ← "age" 写了两遍
  job: job        // ← "job" 写了两遍
};
console.log(person);   // { name: '张三', age: 25, job: '前端工程师' }

// ========== ES6 写法：属性简写，只写一遍 ==========
const name = '张三';
const age = 25;
const job = '前端工程师';

const person = {
  name,            // ← 等价于 name: name
  age,             // ← 等价于 age: age
  job              // ← 等价于 job: job
};
console.log(person);   // { name: '张三', age: 25, job: '前端工程师' }


// 实际应用场景：函数返回对象
// ES5
function createUser(name, age) {
  return {
    name: name,
    age: age,
    createdAt: new Date()
  };
}

// ES6
function createUser(name, age) {
  return {
    name,             // 简洁！
    age,              // 简洁！
    createdAt: new Date()
  };
}

// 箭头函数版本
const createUser = (name, age) => ({ name, age, createdAt: new Date() });
//                                  ↑ 注意：返回对象要用括号包裹 {}
```

---

### 2.2 方法简写（Method Shorthand）

对象里的方法定义也可以省掉 `: function`。

#### ES5 vs ES6 对比

```javascript
// ========== ES5 写法：方法要加 function 关键字 ==========
var person = {
  name: '李四',
  sayHello: function() {           // ← "function" 关键字不可少
    console.log('你好，我是' + this.name);
  },
  getInfo: function() {            // ← 每个方法都要写 function
    return '姓名：' + this.name;
  }
};
person.sayHello();     // "你好，我是李四"

// ========== ES6 写法：直接写方法名 + 括号 ==========
const person = {
  name: '李四',
  sayHello() {                      // ← 省掉了 `: function`
    console.log(`你好，我是${this.name}`);
  },
  getInfo() {                       // ← 更简洁！
    return `姓名：${this.name}`;
  }
};
person.sayHello();     // "你好，我是李四"
```

#### 一个重要的区别：简写方法 vs 箭头函数

```javascript
const obj = {
  name: '测试',

  // 方法简写 —— this 指向 obj（正确！）
  shorthandMethod() {
    console.log(this.name);       // "测试"
  },

  // 箭头函数 —— this 指向外层作用域（可能不是你想要的！）
  arrowMethod: () => {
    console.log(this.name);       // undefined（this 不指向 obj！）
  }
};

obj.shorthandMethod();   // ✅ "测试"
obj.arrowMethod();       // ❌ undefined

// ⚠️ 坑点：在对象中定义方法，要用简写语法，不要用箭头函数！
// 箭头函数没有自己的 this，它会捕获外层的 this
```

---

## 三、计算属性名（Computed Property Names）

### 3.1 为什么需要计算属性名？

有时候对象的属性名不是固定的，而是需要动态生成的（比如根据变量值）。ES5 中只能在对象创建后再用方括号赋值，ES6 允许在对象字面量中直接使用表达式作为属性名。

#### ES5 vs ES6 对比

```javascript
// ========== ES5：只能先创建对象，再动态添加属性 ==========
var propName = 'dynamicKey';
var obj = {};                    // 先创建空对象
obj[propName] = '动态值';         // 再用方括号赋值
obj['prefix_' + propName] = '带前缀的值';  // 表达式也可以
console.log(obj);
// { dynamicKey: '动态值', prefix_dynamicKey: '带前缀的值' }

// ========== ES6：在对象字面量中直接写表达式 ==========
const propName = 'dynamicKey';
const obj = {
  [propName]: '动态值',                  // ← [变量] 作为属性名
  ['prefix_' + propName]: '带前缀的值',   // ← [表达式] 也可以！
  [Date.now()]: '时间戳做属性名',          // ← 甚至可以调用函数！
  ['say' + 'Hello']() {                  // ← 方法名也可以是表达式！
    return 'Hello!';
  }
};
console.log(obj);
// {
//   dynamicKey: '动态值',
//   prefix_dynamicKey: '带前缀的值',
//   '1717654321098': '时间戳做属性名',
//   sayHello: [Function]
// }
```

### 3.2 实际应用场景

```javascript
// 场景：根据 action type 动态生成 reducer 对象
const SET_NAME = 'user/SET_NAME';
const SET_AGE = 'user/SET_AGE';

// ES6 计算属性名让代码结构更清晰
const userReducer = {
  [SET_NAME](state, action) {
    return { ...state, name: action.payload };
  },
  [SET_AGE](state, action) {
    return { ...state, age: action.payload };
  }
};

// 调用
const newState = userReducer[SET_NAME](
  { name: '', age: 0 },
  { payload: '张三' }
);
console.log(newState);       // { name: '张三', age: 0 }


// 场景：合并多个对象的属性计数
const fruits = ['苹果', '香蕉', '苹果', '橘子', '香蕉', '苹果'];

// 用计算属性名优雅地统计出现次数
const count = fruits.reduce((acc, fruit) => {
  return {
    ...acc,
    [fruit]: (acc[fruit] || 0) + 1    // 动态属性名累加
  };
}, {});
console.log(count);          // { 苹果: 3, 香蕉: 2, 橘子: 1 }
```

---

## 四、Object.assign() —— 对象合并

### 4.1 基本用法

`Object.assign()` 用于将一个或多个源对象的**可枚举属性**复制到目标对象中。

```javascript
// 语法：Object.assign(target, ...sources)
// 把 source1, source2... 的属性复制到 target 中
// 返回 target（修改后的目标对象）

const target = { a: 1, b: 2 };
const source = { b: 3, c: 4 };

const result = Object.assign(target, source);

console.log(result);     // { a: 1, b: 3, c: 4 }
console.log(target);     // { a: 1, b: 3, c: 4 }  ← target 也被修改了！
//          ↑ ⚠️ 注意：target 本身被修改了，result === target
```

#### ES5 vs ES6 对比：合并对象

```javascript
// ========== ES5：手动循环合并 ==========
var defaults = { theme: 'light', lang: 'zh', showAds: true };
var userSettings = { theme: 'dark' };

var settings = {};
for (var key in defaults) {
  if (defaults.hasOwnProperty(key)) {
    settings[key] = defaults[key];
  }
}
for (var key in userSettings) {
  if (userSettings.hasOwnProperty(key)) {
    settings[key] = userSettings[key];   // 用户设置覆盖默认设置
  }
}
console.log(settings);     // { theme: 'dark', lang: 'zh', showAds: true }

// ========== ES6：Object.assign() 一行搞定 ==========
const defaults = { theme: 'light', lang: 'zh', showAds: true };
const userSettings = { theme: 'dark' };

// 后面的属性会覆盖前面的同名属性
const settings = Object.assign({}, defaults, userSettings);
//                           ↑ 空对象作为目标，避免修改 defaults
console.log(settings);     // { theme: 'dark', lang: 'zh', showAds: true }
console.log(defaults);     // { theme: 'light', lang: 'zh', showAds: true } ✅ 未被修改
```

### 4.2 核心重点：浅拷贝 vs 深拷贝 ⚠️

这是 `Object.assign()` 最重要、最容易踩坑的地方！

#### 浅拷贝的含义

`Object.assign()` 是**浅拷贝（Shallow Copy）**。它只复制属性值，如果属性值是引用类型（对象、数组），复制的是引用（内存地址），而不是创建新的副本。

```javascript
// ========== 浅拷贝的坑 ==========
const obj1 = {
  name: '张三',
  hobbies: ['读书', '游泳'],     // ← 数组是引用类型
  address: {                     // ← 对象也是引用类型
    city: '北京',
    zip: '100000'
  }
};

const obj2 = Object.assign({}, obj1);

// 基本类型的修改互不影响
obj2.name = '李四';
console.log(obj1.name);          // "张三" ✅ 没受影响

// 引用类型的修改会互相影响！⚠️
obj2.hobbies.push('跑步');
console.log(obj1.hobbies);       // ["读书", "游泳", "跑步"] ❌ obj1 也被改了！
console.log(obj2.hobbies);       // ["读书", "游泳", "跑步"]
//    ↑ 因为 obj1.hobbies 和 obj2.hobbies 指向同一个数组！

obj2.address.city = '上海';
console.log(obj1.address.city);  // "上海" ❌ obj1 的地址也被改了！
```

用一张图来理解：

```
浅拷贝前：                    浅拷贝后（Object.assign）：
┌─────────────┐              ┌─────────────┐
│   obj1      │              │    obj1     │
│  name: "张" │              │  name: "张" │
│  hobbies ───┼──→ [读书,游泳] │  hobbies ───┼──┐
│  address ───┼──→ {city:北京} │  address ───┼──┼──→ {city:北京}
└─────────────┘              └─────────────┘  │
                              ┌─────────────┐ │
                              │    obj2     │ │
                              │  name: "张" │ │
                              │  hobbies ───┼─┘   ← 指向同一个数组！
                              │  address ───┘     ← 指向同一个对象！
                              └─────────────┘
```

#### 如何实现深拷贝？

```javascript
const obj = {
  name: '张三',
  hobbies: ['读书', '游泳'],
  address: { city: '北京', zip: '100000' },
  date: new Date(),
  fn: function() { return 'hello'; }
};

// ========== 方法 1：JSON 序列化（有局限）==========
const deep1 = JSON.parse(JSON.stringify(obj));
// 优点：简单，能实现多层深拷贝
// 缺点：
// 1. 丢失函数（function 不会被序列化）
// 2. 丢失 Date 类型（变成字符串）
// 3. 丢失 undefined、RegExp、Map、Set 等
// 4. 不能处理循环引用

console.log(deep1.hobbies === obj.hobbies);     // false ✅ 不同引用了
console.log(deep1.address === obj.address);     // false ✅
console.log(typeof deep1.fn);                    // "undefined" ❌ 函数丢了！
console.log(typeof deep1.date);                  // "string"  ❌ Date 变字符串了

// ========== 方法 2：递归实现（最可靠）==========
function deepClone(obj, hash = new WeakMap()) {
  // 处理 null 或非对象
  if (obj === null || typeof obj !== 'object') return obj;

  // 处理 Date
  if (obj instanceof Date) return new Date(obj);

  // 处理 RegExp
  if (obj instanceof RegExp) return new RegExp(obj);

  // 处理循环引用
  if (hash.has(obj)) return hash.get(obj);

  // 创建新对象/数组
  const clone = Array.isArray(obj) ? [] : {};
  hash.set(obj, clone);

  // 递归复制每个属性
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      clone[key] = deepClone(obj[key], hash);
    }
  }
  return clone;
}

const deep2 = deepClone(obj);
console.log(deep2.hobbies === obj.hobbies);     // false ✅
console.log(deep2.address === obj.address);     // false ✅
console.log(typeof deep2.fn);                    // "function" ✅ 保留了！
console.log(deep2.date instanceof Date);         // true ✅ Date 类型保留了

// ========== 方法 3：现代方案 —— structuredClone（推荐，浏览器/Node 17+）==========
// const deep3 = structuredClone(obj);   // 原生深拷贝，但有限制（不能复制函数）

// ========== 方法 4：Lodash 的 cloneDeep（最省心）==========
// const deep4 = _.cloneDeep(obj);       // 功能最全，但需要引入库
```

#### 深拷贝方案对比表

| 方案 | 优点 | 缺点 | 推荐场景 |
|------|------|------|---------|
| `Object.assign()` | 原生、快 | 浅拷贝 | 对象只有基本类型属性时 |
| `JSON.parse/stringify` | 最简单 | 丢失函数、Date、undefined | 纯数据对象（JSON 安全） |
| 递归 `deepClone` | 最完整 | 代码多、有性能开销 | 需要完整深拷贝的复杂对象 |
| `structuredClone` | 原生深拷贝 | 不能复制函数、需新环境 | 现代浏览器/Node 环境 |
| `_.cloneDeep` | 功能最全 | 需引入 Lodash 库 | 项目已使用 Lodash |

### 4.3 Object.assign 的其他应用

```javascript
// 1. 对象克隆（浅拷贝）
const clone = Object.assign({}, original);

// 2. 添加/覆盖多个属性
const user = { name: '张三' };
Object.assign(user, { age: 25 }, { job: '工程师' });
console.log(user);           // { name: '张三', age: 25, job: '工程师' }

// 3. 为对象添加默认值
function createConfig(options) {
  const defaults = { host: 'localhost', port: 8080, debug: false };
  return Object.assign({}, defaults, options);
  //                                ↑ options 的属性会覆盖 defaults
}
console.log(createConfig({ port: 3000 }));
// { host: 'localhost', port: 3000, debug: false }
```

---

## 五、对象展开运算符（Object Spread Operator）

对象展开运算符 `{...obj}` 是 `Object.assign()` 的语法糖，让对象复制和合并更加优雅。它是 ES2018 引入的特性，但已经被广泛支持。

### 5.1 基本用法

```javascript
// ========== Object.assign 写法 ==========
const obj1 = { a: 1, b: 2 };
const obj2 = { b: 3, c: 4 };
const merged = Object.assign({}, obj1, obj2);
console.log(merged);         // { a: 1, b: 3, c: 4 }

// ========== 展开运算符写法（更简洁！）==========
const obj1 = { a: 1, b: 2 };
const obj2 = { b: 3, c: 4 };
const merged = { ...obj1, ...obj2 };
//              ↑ 把 obj1 的属性"展开"进来
//                      ↑ 再把 obj2 的属性"展开"进来（后面的覆盖前面的）
console.log(merged);         // { a: 1, b: 3, c: 4 }
```

### 5.2 展开运算符的优势

```javascript
// 1. 代码更易读，语义更清晰
const config = Object.assign(
  {},
  defaultConfig,
  envConfig,
  userConfig
);

// vs
const config = {
  ...defaultConfig,
  ...envConfig,
  ...userConfig
};


// 2. 可以方便地覆盖或添加单个属性
const user = { name: '张三', age: 25 };
const updated = { ...user, age: 26, job: '工程师' };
//                           ↑ 覆盖 age
//                                  ↑ 新增 job
console.log(updated);        // { name: '张三', age: 26, job: '工程师' }
console.log(user);           // { name: '张三', age: 25 } ✅ 原对象不变


// 3. 可以方便地"删除"属性（通过解构 + 展开）
const user = { name: '张三', password: 'secret123', age: 25 };

// 解构出 password，其余属性展开到新对象
const { password, ...safeUser } = user;
//      ↑ 取出 password 变量（后面不用它）
//            ↑ 剩余的所有属性收集到 safeUser
console.log(safeUser);       // { name: '张三', age: 25 }
// password 属性被"剔除"了


// 4. 与数组展开组合使用
const person = { name: '李四', skills: ['JS', 'CSS'] };
const copy = {
  ...person,
  skills: [...person.skills, 'HTML']   // 数组也要展开才能深拷贝
};
copy.skills.push('React');
console.log(person.skills);  // ['JS', 'CSS'] ✅ 原数组没变
console.log(copy.skills);    // ['JS', 'CSS', 'HTML', 'React']
```

### 5.3 ⚠️ 同样是浅拷贝！

```javascript
const obj = {
  inner: { value: 10 }
};

const copy = { ...obj };
copy.inner.value = 20;

console.log(obj.inner.value);   // 20 ❌ 和 Object.assign 一样的浅拷贝问题

// 需要深拷贝时，要递归展开每一层
const deep = {
  ...obj,
  inner: { ...obj.inner }       // 手动展开嵌套对象
};
deep.inner.value = 30;
console.log(obj.inner.value);   // 20 ✅ 这次没受影响
```

### 5.4 Object.assign vs 展开运算符对比

| 特性 | `Object.assign()` | `{...obj}` 展开运算符 |
|------|------------------|---------------------|
| 语法 | 函数调用 | 语法糖，更简洁 |
| 空对象开头 | 需要 `Object.assign({}, ...)` | 天然不修改原对象 |
| 展开 getter | 执行 getter 获取值 | 执行 getter 获取值 |
| 复制 Symbol | ✅ 支持 | ✅ 支持 |
| 设置原型 | 不能 | 不能 |
| 可读性 | 一般 | 极佳 |
| 兼容性 | ES2015 | ES2018 |

> **推荐**：优先使用展开运算符 `{...obj}`，代码更简洁直观。只有在需要利用 `Object.assign()` 的返回值或兼容旧环境时才使用后者。

---

## 六、Object 的新方法

ES6 为 `Object` 构造函数增加了几个非常实用的静态方法，让对象操作更加便利。

### 6.1 Object.keys() —— 获取所有键

返回对象自身**可枚举属性**的键名数组。

```javascript
const user = {
  name: '张三',
  age: 25,
  job: '工程师'
};

const keys = Object.keys(user);
console.log(keys);           // ['name', 'age', 'job']

// ========== ES5 vs ES6 对比 ==========
// ES5 中需要手动遍历
var keysES5 = [];
for (var key in user) {
  if (user.hasOwnProperty(key)) {    // 别忘了 hasOwnProperty！
    keysES5.push(key);
  }
}

// ES6 一行搞定
const keysES6 = Object.keys(user);
```

### 6.2 Object.values() —— 获取所有值

返回对象自身**可枚举属性**的键值数组。这是 ES2017 新增的方法。

```javascript
const user = {
  name: '张三',
  age: 25,
  job: '工程师'
};

const values = Object.values(user);
console.log(values);         // ['张三', 25, '工程师']

// ========== ES5 的笨拙实现 ==========
var valuesES5 = Object.keys(user).map(function(key) {
  return user[key];
});

// ========== ES6 优雅实现 ==========
const valuesES6 = Object.values(user);
```

### 6.3 Object.entries() —— 获取所有键值对

返回对象自身**可枚举属性**的 `[key, value]` 数组。这是 ES2017 新增的方法，非常实用。

```javascript
const user = {
  name: '张三',
  age: 25,
  job: '工程师'
};

const entries = Object.entries(user);
console.log(entries);
// [
//   ['name', '张三'],
//   ['age', 25],
//   ['job', '工程师']
// ]
```

#### entries 的经典应用场景

```javascript
// 场景 1：把对象转为 Map
const user = { name: '张三', age: 25 };
const map = new Map(Object.entries(user));
console.log(map.get('name'));    // "张三"

// 场景 2：配合 for...of 遍历对象
for (const [key, value] of Object.entries(user)) {
  console.log(`${key}: ${value}`);
}
// name: 张三
// age: 25

// 场景 3：过滤对象属性
const scores = { 数学: 90, 英语: 58, 物理: 85, 化学: 55 };

// 找出不及格的科目
const failed = Object.entries(scores)
  .filter(([subject, score]) => score < 60)
  .map(([subject]) => subject);
console.log(failed);         // ['英语', '化学']

// 或者用 Object.fromEntries 转回对象（ES2019）
const passed = Object.fromEntries(
  Object.entries(scores).filter(([, score]) => score >= 60)
);
console.log(passed);         // { 数学: 90, 物理: 85 }
```

### 6.4 三个方法对比总结

```javascript
const obj = { a: 1, b: 2, c: 3 };

Object.keys(obj);      // ['a', 'b', 'c']        ← 只取键
Object.values(obj);    // [1, 2, 3]              ← 只取值
Object.entries(obj);   // [['a',1],['b',2],['c',3]]  ← 键值对
```

| 方法 | 返回值类型 | 返回内容 | 适用场景 |
|------|-----------|---------|---------|
| `Object.keys(obj)` | `string[]` | 所有键名 | 遍历键、检查属性存在 |
| `Object.values(obj)` | `any[]` | 所有键值 | 只需要值的时候 |
| `Object.entries(obj)` | `[string, any][]` | 键值对数组 | 需要同时用键和值 |

### 6.5 for...in vs Object.keys/values/entries

```javascript
const obj = { a: 1, b: 2 };

// 定义一个原型对象
const proto = { inherited: '我是继承来的' };
Object.setPrototypeOf(obj, proto);

// for...in 会遍历继承的属性
for (const key in obj) {
  console.log(key);        // 'a', 'b', 'inherited'  ← 包含继承属性！
}

// Object.keys/values/entries 只遍历自身属性
console.log(Object.keys(obj));       // ['a', 'b']  ← 不包含继承属性
console.log(Object.values(obj));     // [1, 2]
console.log(Object.entries(obj));    // [['a', 1], ['b', 2]]

// ⚠️ 总结：for...in 需要配合 hasOwnProperty，新方法更安全
```

---

## 七、本章知识回顾

### 7.1 核心知识点速查表

| 类别 | 知识点 | 关键记忆点 |
|------|--------|-----------|
| **数组查找** | `find()` / `findIndex()` | 返回第一个匹配项（元素/索引），无则返回 `undefined`/`-1` |
| **数组判断** | `includes()` | 返回布尔值，能正确判断 `NaN` |
| **数组转换** | `Array.from()` | 类数组/可迭代 → 真数组，可用映射函数 |
| **数组创建** | `Array.of()` | 无歧义地创建数组，解决 `new Array(3)` 的坑 |
| **对象简写** | `{name}` / `sayHi(){}` | 变量名=属性名时可简写，方法省略 `:function` |
| **计算属性** | `[expr]` | 方括号内可以放变量或表达式作为属性名 |
| **对象合并** | `Object.assign()` | 浅拷贝！后面的覆盖前面的，注意引用类型 |
| **对象展开** | `{...obj}` | `assign` 的语法糖，更简洁，同样是浅拷贝 |
| **遍历对象** | `keys/values/entries` | 三个方法各司其职，返回数组方便链式调用 |

### 7.2 最需要注意的坑

1. **`find()` vs `filter()`**：`find` 返回第一个匹配元素，`filter` 返回所有匹配元素的**数组**
2. **`includes()` vs `indexOf()`**：优先用 `includes()`，语义更清晰，且能判断 `NaN`
3. **浅拷贝陷阱**：`Object.assign()` 和 `{...obj}` 都是浅拷贝，嵌套对象会共享引用
4. **箭头函数做方法**：对象方法用简写语法 `sayHi(){}`，不要用箭头函数 `sayHi: () => {}`
5. **`Array.from({length: n})`**：可以用来快速生成序列，配合映射函数非常强大

### 7.3 最佳实践速记

```javascript
// ✅ 查找用 find
const user = users.find(u => u.id === targetId);

// ✅ 判断存在用 includes
if (arr.includes(value)) { ... }

// ✅ 类数组转数组用 Array.from
const arr = Array.from(nodeList);

// ✅ 对象合并用展开运算符
const merged = { ...defaults, ...options };

// ✅ 浅拷贝用展开运算符
const copy = { ...original };

// ✅ 深拷贝用递归或第三方库
const deep = deepClone(original);  // 或 _.cloneDeep(original)

// ✅ 遍历对象用 entries
for (const [key, val] of Object.entries(obj)) { ... }
```

---

## 八、课后练习

### 练习 1：数组查找

```javascript
const products = [
  { id: 101, name: 'iPhone', price: 5999, category: '手机' },
  { id: 102, name: 'iPad', price: 3999, category: '平板' },
  { id: 103, name: 'MacBook', price: 9999, category: '电脑' },
  { id: 104, name: 'AirPods', price: 1299, category: '配件' },
  { id: 105, name: '小米13', price: 3999, category: '手机' }
];

// 1. 找到第一个价格低于 4000 的产品
// 2. 找到第一个手机类别的索引
// 3. 判断是否包含 id 为 103 的产品（用 includes 思路，提示：先 map 再 includes）
```

### 练习 2：对象操作

```javascript
const student = {
  name: '小明',
  scores: { math: 90, english: 75, science: 85 },
  hobbies: ['篮球', '编程']
};

// 1. 用展开运算符创建 student 的浅拷贝
// 2. 修改拷贝中的 math 分数为 95，检查原对象是否受影响
// 3. 如何用深拷贝正确复制这个对象？
```

### 练习 3：综合运用

```javascript
// 将下面的配置合并函数用 ES6 写法简化
function mergeConfig(defaults, userConfig) {
  var result = {};
  for (var key in defaults) {
    result[key] = defaults[key];
  }
  for (var key in userConfig) {
    if (typeof userConfig[key] === 'object' && userConfig[key] !== null) {
      result[key] = mergeConfig(defaults[key] || {}, userConfig[key]);
    } else {
      result[key] = userConfig[key];
    }
  }
  return result;
}

// 尝试用 Object.assign 或展开运算符改写
// 思考：上面的函数其实已经实现了一个简单的深拷贝合并，
// Object.assign 和展开运算符能做到同样的效果吗？为什么？
```

---

> **本章小结**：这一章我们系统学习了 ES6 对数组和对象的扩展。数组的新方法让查找、转换、判断更加简洁；对象的简写和计算属性让代码更优雅；`Object.assign` 和展开运算符让对象合并变得轻而易举。但请记住——**浅拷贝的坑无处不在**，处理嵌套对象时一定要多加小心。下一章，我们将进入 ES6 最激动人心的部分——**Promise 与异步编程**，带你彻底告别回调地狱！

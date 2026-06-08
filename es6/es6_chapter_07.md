# 第七章：其他常用特性

> **章节导读**：前面几章我们已经学习了ES6最核心的特性——箭头函数、解构赋值、类、模块、Promise和async/await。本章将带你认识ES6中同样重要但相对"独立"的特性：两个强大的新数据结构`Map`和`Set`、独一无二的`Symbol`类型、优雅的`for...of`循环，以及迭代器机制。这些特性就像你工具箱里的各种精巧工具，虽然不常用，但用对了地方就能事半功倍。

---

## 7.1 Map —— 升级版的数据收纳盒（键值对存储）

### 7.1.1 为什么需要Map？

想象你有一个**普通抽屉（Object）**，你用它来存放各种物品。但抽屉有几个固有的限制：

- 只能贴**字符串标签**（或Symbol）来标识物品
- 抽屉自带了一些"系统标签"（如`toString`、`constructor`），你可能不小心跟它们冲突
- 你没法轻松知道里面到底放了多少件东西

```javascript
// 用Object当"抽屉"的尴尬
var drawer = {};

// 想用一个对象当钥匙？不行，会被转成字符串"[object Object]"
var key = { id: 1 };
drawer[key] = '重要文件';

console.log(drawer['[object Object]']); // "重要文件" —— 钥匙变成了字符串！
console.log(drawer[key]);               // "重要文件" —— 巧合能取到，但不可靠

// 不小心跟原型链上的属性冲突
drawer.toString = '我的数据';
console.log(drawer.toString); // "我的数据" —— 覆盖了继承的方法！
```

ES6推出的`Map`，就是一个**专业级的数据收纳盒**：

| 特性 | Object（普通抽屉） | Map（专业收纳盒） |
|------|------|------|
| 键的类型 | 只能是字符串或Symbol | **任意类型**（对象、函数、NaN都可以） |
| 键值对顺序 | 不保证（整数键会排序） | **保证插入顺序** |
| 获取大小 | 手动遍历 `Object.keys()` | `.size` 属性直接获取 |
| 迭代便利性 | 需要借助`for...in`或`Object.entries()` | **内置迭代器**，直接用`for...of` |
| 原型链污染 | 有（可能跟继承属性冲突） | **无**（纯净的数据容器） |
| 性能（频繁增删） | 一般 | **优化过**，更适合频繁增删 |
| 序列化 | `JSON.stringify()`支持 | 不支持原生序列化 |

### 7.1.2 Map的基本用法

```javascript
// ===== ES5：用Object勉为其难 =====
var userAges = {};
var userKey = { name: '张三' };

// 对象当键？被转成"[object Object]"
userAges[userKey] = 25;
console.log(userAges['[object Object]']); // 25 —— 尴尬！

// ===== ES6：Map轻松搞定 =====
const userAgesMap = new Map();
const userObj = { name: '张三' };

// 任何类型都能当键！
userAgesMap.set(userObj, 25);
userAgesMap.set('李四', 30);           // 字符串键
userAgesMap.set(123, '编号用户');      // 数字键
userAgesMap.set(NaN, '特殊用户');      // NaN也能当键！

console.log(userAgesMap.get(userObj)); // 25 —— 完美取回！
console.log(userAgesMap.get(NaN));     // "特殊用户"
console.log(userAgesMap.size);         // 4 —— 一目了然有多少条

// 链式调用
const map = new Map();
map.set('a', 1)
   .set('b', 2)
   .set('c', 3);  // 链式设置，一气呵成

console.log(map.get('b')); // 2
```

### 7.1.3 Map的常用方法

```javascript
const m = new Map();

// --- 增 ---
m.set('name', '小明');
m.set('age', 18);

// --- 查 ---
m.has('name');        // true —— 是否存在这个键
m.get('name');        // "小明" —— 取值
m.get('不存在的键');   // undefined —— 不存在返回undefined

// --- 删 ---
m.delete('age');      // true —— 删除成功返回true
m.delete('不存在');    // false —— 删除失败返回false
m.clear();            // 清空所有

// --- 遍历 ---
m.set('a', 1);
m.set('b', 2);
m.set('c', 3);

// 1. forEach
m.forEach((value, key) => {
  console.log(`${key}: ${value}`);
});
// 输出:
// a: 1
// b: 2
// c: 3

// 2. for...of（后面会详细讲）
for (const [key, value] of m) {
  console.log(`${key} = ${value}`);
}

// 3. 只遍历键
for (const key of m.keys()) {
  console.log(key); // a, b, c
}

// 4. 只遍历值
for (const value of m.values()) {
  console.log(value); // 1, 2, 3
}

// 5. 遍历键值对
for (const entry of m.entries()) {
  console.log(entry); // ['a', 1], ['b', 2], ['c', 3]
}
```

### 7.1.4 Map的初始化

```javascript
// 方式1：二维数组初始化
const map1 = new Map([
  ['name', '小明'],
  ['age', 18],
  ['city', '北京']
]);
console.log(map1.get('name')); // "小明"

// 方式2：从已有Map复制
const map2 = new Map(map1);
console.log(map2.size); // 3

// 方式3：从Object转换
const obj = { foo: 'bar', baz: 42 };
// Object.entries() 返回 [['foo','bar'],['baz',42]]
const map3 = new Map(Object.entries(obj));
console.log(map3.get('foo')); // "bar"

// Map转回Object
const backToObj = Object.fromEntries(map3);
console.log(backToObj); // { foo: "bar", baz: 42 }
```

### 7.1.5 WeakMap —— 弱引用版本

`WeakMap`是`Map`的特殊版本，它的键**必须是对象**，并且对这些对象是**弱引用**——不影响垃圾回收。

```javascript
// ===== WeakMap的用途：私有数据存储 =====

// ES6写法：用WeakMap实现真正的私有属性
const privateData = new WeakMap();

class Person {
  constructor(name, secret) {
    // 公开的
    this.name = name;
    // 私存的——外部无法直接访问
    privateData.set(this, { secret: secret });
  }

  revealSecret() {
    // 只能通过方法访问私有数据
    return privateData.get(this).secret;
  }
}

const p = new Person('张三', '我有一个秘密');
console.log(p.name);           // "张三" —— 公开属性可以访问
console.log(p.secret);         // undefined —— 不存在这个属性！
console.log(p.revealSecret()); // "我有一个秘密" —— 通过方法才能拿到
```

> **WeakMap vs Map 关键区别**：
> - `WeakMap`的键必须是对象，原始类型不行
> - `WeakMap`不可遍历（没有`size`、`keys()`、`values()`、`entries()`、`forEach`）
> - `WeakMap`只有`set`、`get`、`has`、`delete`四个方法
> - 当`WeakMap`的键对象不再被其他地方引用时，垃圾回收器会自动回收对应的键值对

### 7.1.6 什么时候用Map？

| 场景 | 推荐选择 | 理由 |
|------|------|------|
| 键类型不确定（可能是对象、函数） | **Map** | Object只支持字符串/Symbol键 |
| 需要频繁增删键值对 | **Map** | 性能优化过 |
| 需要保持插入顺序 | **Map** | Map保证顺序 |
| 需要知道键值对数量 | **Map** | `.size`即取即用 |
| 纯数据存储，无逻辑方法 | **Map** | 无原型链污染 |
| 简单的配置对象、JSON数据 | Object | 更轻量，支持序列化 |
| 需要`JSON.stringify` | Object | Map不支持原生序列化 |
| 需要枚举属性（`for...in`） | Object | 传统习惯 |

---

## 7.2 Set —— 去重利器（唯一值集合）

### 7.2.1 为什么需要Set？

想象你有一个**集邮册**，每种类型的邮票你只需要一张。传统方式（数组）就像一个**随便放的盒子**，里面可能有重复的邮票，你需要自己手动检查是否已经存在。

`Set`就像一个**智能集邮册**——它会自动帮你过滤重复的值，保证每一张都是独一无二的。

```javascript
// ===== ES5：手动去重，麻烦又容易出错 =====
var numbers = [1, 2, 2, 3, 3, 3, 4];
var unique = [];

for (var i = 0; i < numbers.length; i++) {
  if (unique.indexOf(numbers[i]) === -1) {
    unique.push(numbers[i]);
  }
}
console.log(unique); // [1, 2, 3, 4] —— 代码写了一大段

// 或者用对象当哈希表去重（更hack）
var hash = {};
var unique2 = numbers.filter(function(item) {
  var key = JSON.stringify(item);
  return hash.hasOwnProperty(key) ? false : (hash[key] = true);
});

// ===== ES6：Set一行搞定 =====
const uniqueSet = [...new Set([1, 2, 2, 3, 3, 3, 4])];
console.log(uniqueSet); // [1, 2, 3, 4] —— 就是这么优雅！
```

### 7.2.2 Set的基本方法

```javascript
const set = new Set();

// --- 增 ---
set.add(1);
set.add(2);
set.add(1); // 重复的值会被忽略
console.log(set.size); // 2 —— 1只存了一份

// 链式调用
set.add(3).add(4).add(5);

// --- 查 ---
set.has(1);     // true
set.has(100);   // false

// --- 删 ---
set.delete(1);  // true —— 删除成功
set.delete(99); // false —— 不存在则返回false
// set.clear(); // 清空所有

// --- 遍历 ---
for (const value of set) {
  console.log(value); // 2, 3, 4, 5
}

// forEach（注意：Set的forEach参数是 (value, value, set)）
set.forEach((value, alsoValue, theSet) => {
  // 为了保持与Map的forEach签名一致：forEach(value, key, collection)
  // Set的value和key是同一个值
  console.log(value); // 2, 3, 4, 5
});
```

### 7.2.3 Set初始化与实用技巧

```javascript
// 从数组初始化
const set1 = new Set([1, 2, 2, 3, 3, 3]);
console.log([...set1]); // [1, 2, 3]

// 字符串去重（每个字符是一个元素）
const uniqueChars = [...new Set('hello')].join('');
console.log(uniqueChars); // "helo"

// 对象数组去重？Set不能自动判断对象相等！
const set2 = new Set([{a: 1}, {a: 1}]);
console.log(set2.size); // 2 —— 两个对象引用不同，Set认为这是两个不同的值

// 基本类型去重——完美工作
const mixedSet = new Set([1, '1', 1, true, 'true', NaN, NaN]);
console.log([...mixedSet]); // [1, "1", true, "true", NaN]
// 注意：1 !== '1'，true !== 'true'，但NaN === NaN（Set特殊处理）
```

### 7.2.4 Set的集合运算

```javascript
const a = new Set([1, 2, 3, 4]);
const b = new Set([3, 4, 5, 6]);

// 交集（两个集合共有的）
const intersection = new Set([...a].filter(x => b.has(x)));
console.log([...intersection]); // [3, 4]

// 并集（两个集合所有的，去重）
const union = new Set([...a, ...b]);
console.log([...union]); // [1, 2, 3, 4, 5, 6]

// 差集（在a中但不在b中的）
const difference = new Set([...a].filter(x => !b.has(x)));
console.log([...difference]); // [1, 2]

// 对称差集（只在其中一个集合中的）
const symDiff = new Set([...a, ...b].filter(x => a.has(x) ^ b.has(x)));
console.log([...symDiff]); // [1, 2, 5, 6]
```

### 7.2.5 WeakSet —— 对象的专属集合

```javascript
// WeakSet只能存对象，不能存原始值
const ws = new WeakSet();

const obj1 = { name: 'A' };
const obj2 = { name: 'B' };

ws.add(obj1);
ws.add(obj2);

console.log(ws.has(obj1)); // true

ws.delete(obj1);
console.log(ws.has(obj1)); // false

// WeakSet的应用：标记对象
const visited = new WeakSet();

function process(obj) {
  if (visited.has(obj)) {
    console.log('已经处理过了，跳过');
    return;
  }
  visited.add(obj);
  console.log('处理对象:', obj);
}

process(obj2); // "处理对象: { name: 'B' }"
process(obj2); // "已经处理过了，跳过"
// 当obj2不再被引用时，visited中的记录会自动被垃圾回收
```

> **Set vs Array 速查**：
> - `Set`自动去重，`Array`允许重复
> - `Set`查找元素用`.has()`，时间复杂度O(1)；`Array`用`.includes()`或`.indexOf()`，时间复杂度O(n)
> - `Set`没有索引，不能通过`set[0]`访问；`Array`可以
> - `Set`没有`.map()`、`.filter()`等方法，需要转成`Array`再操作：`[...set].filter(...)`
> - 需要频繁查找是否存在某元素时，`Set`比`Array`更高效

---

## 7.3 Symbol —— 独一无二的身份证

### 7.3.1 为什么需要Symbol？

想象你要给一个**公共对象**添加属性，但你担心跟别人添加的属性**重名**。Symbol就是解决这个问题的——它创建的是**独一无二的标识符**，永远不会跟别人冲突。

```javascript
// 场景：你写了一个库，要给用户传入的对象加一个"标记"
// 如果用字符串，万一用户对象已经有这个属性呢？

// ===== ES5：字符串属性名容易冲突 =====
var MAGIC_KEY = '__my_library_hidden_key__';
var obj = {};

obj[MAGIC_KEY] = '内部数据';
// 风险：万一用户也用了同样的字符串？虽然概率小，但不是零！

// ===== ES6：Symbol彻底杜绝冲突 =====
const MAGIC_KEY = Symbol('my_library_key');
const obj2 = {};

obj2[MAGIC_KEY] = '内部数据';
// 这个属性名是全球唯一的，100%不会跟别人冲突！
```

### 7.3.2 Symbol的基本用法

```javascript
// 创建一个Symbol
const s1 = Symbol();
const s2 = Symbol();

console.log(s1 === s2); // false —— 每个Symbol都是独一无二的！

// 可以传一个描述字符串（调试用，不影响唯一性）
const s3 = Symbol('描述');
const s4 = Symbol('描述'); // 同样的描述

console.log(s3 === s4);           // false —— 描述相同，但仍是不同的Symbol
console.log(s3.toString());       // "Symbol(描述)"
console.log(s4.description);      // "描述" —— ES2019新增的.description属性

// typeof检测
console.log(typeof s1); // "symbol" —— 全新的基本数据类型！
```

### 7.3.3 Symbol作为对象属性

```javascript
// ===== ES5：属性名只能是字符串 =====
var es5Obj = {};
es5Obj['name'] = '小明';
es5Obj['age'] = 18;
// for...in会遍历到所有可枚举字符串属性

// ===== ES6：Symbol作为属性名 =====
const id = Symbol('id');
const grade = Symbol('grade');

const student = {
  name: '小明',
  age: 18,
  [id]: 'S001',        // Symbol属性：必须用方括号定义
  [grade]: 'A'         // Symbol属性
};

// 普通访问
console.log(student[id]);      // "S001" —— 必须用方括号访问，不能用student.id
console.log(student['id']);    // undefined —— 不能用字符串访问

// Symbol属性的特点：
console.log(Object.keys(student));     // ["name", "age"] —— Symbol属性不可枚举！
console.log(JSON.stringify(student));  // "{\"name\":\"小明\",\"age\":18}" —— JSON中会被忽略！

// 获取Symbol属性的方法：
console.log(Object.getOwnPropertySymbols(student)); // [Symbol(id), Symbol(grade)]

// Reflect.ownKeys能获取所有类型的键（包括Symbol）
console.log(Reflect.ownKeys(student)); // ["name", "age", Symbol(id), Symbol(grade)]
```

### 7.3.4 应用场景：实现对象私有属性

```javascript
// ===== ES6：用Symbol实现"伪私有"属性 =====
const _password = Symbol('password');  // 模块内部持有，不导出
const _salary = Symbol('salary');

class Employee {
  constructor(name, password, salary) {
    this.name = name;           // 公开属性
    this[_password] = password; // "私有"属性——外部很难访问到
    this[_salary] = salary;     // "私有"属性
  }

  checkPassword(pwd) {
    return this[_password] === pwd;
  }

  getSalaryLevel() {
    if (this[_salary] > 50000) return '高';
    if (this[_salary] > 10000) return '中';
    return '低';
  }
}

const emp = new Employee('张三', 'secret123', 30000);

console.log(emp.name);             // "张三" —— 公开
console.log(emp[_password]);       // 可以访问，但因为没有导出Symbol，外部不知道这个键
console.log(emp.checkPassword('secret123')); // true

// 常规遍历不到Symbol属性
for (const key in emp) {
  console.log(key); // 只输出 "name"
}
```

### 7.3.5 全局Symbol注册表

```javascript
// Symbol.for()：在全局注册表中创建/获取Symbol
// 相同key返回同一个Symbol（跨文件/iframe共享）
const globalSym1 = Symbol.for('app.config');
const globalSym2 = Symbol.for('app.config');

console.log(globalSym1 === globalSym2); // true —— 同一个Symbol！

// Symbol.keyFor()：反向查找已注册Symbol的key
console.log(Symbol.keyFor(globalSym1)); // "app.config"

// 注意：普通的Symbol不在全局注册表中
const localSym = Symbol('local');
console.log(Symbol.keyFor(localSym)); // undefined

// 应用场景：跨模块共享一个唯一的标识
// 模块A: const CONFIG = Symbol.for('app.config');
// 模块B: const CONFIG = Symbol.for('app.config'); // 获取到同一个Symbol
```

### 7.3.6 内置的Well-Known Symbols

ES6定义了一些内置的Symbol常量，用于控制对象的内部行为：

```javascript
// Symbol.iterator —— 定义对象的默认迭代器（后面会详细讲）
const range = {
  from: 1,
  to: 5,
  [Symbol.iterator]() {
    return {
      current: this.from,
      last: this.to,
      next() {
        return this.current <= this.last
          ? { done: false, value: this.current++ }
          : { done: true };
      }
    };
  }
};

console.log([...range]); // [1, 2, 3, 4, 5] —— 自定义迭代器！

// Symbol.toStringTag —— 控制Object.prototype.toString()的输出
class MyClass {
  get [Symbol.toStringTag]() {
    return 'MyAwesomeClass';
  }
}
const instance = new MyClass();
console.log(Object.prototype.toString.call(instance)); // "[object MyAwesomeClass]"

// Symbol.hasInstance —— 控制 instanceof 的行为
class SpecialArray {
  static [Symbol.hasInstance](instance) {
    return Array.isArray(instance) && instance.length > 0;
  }
}
console.log([] instanceof SpecialArray);      // false —— 空数组
console.log([1, 2] instanceof SpecialArray);  // true —— 非空数组

// 其他内置Symbol：
// Symbol.toPrimitive —— 控制对象转原始值的行为
// Symbol.search/replace/split/match —— 控制对应字符串方法的行为
```

---

## 7.4 for...of 循环 —— 遍历的新姿势

### 7.4.1 for...of vs for...in vs forEach

在ES6之前，我们有各种遍历方式，但各有痛点：

```javascript
var arr = ['a', 'b', 'c'];
arr.foo = '额外属性'; // 给数组加自定义属性（不推荐，但可能发生）

// ===== 传统for循环 —— 最原始 =====
for (var i = 0; i < arr.length; i++) {
  console.log(arr[i]); // a, b, c
}
// 优点：控制最精细
// 缺点：写法繁琐，容易写错索引

// ===== forEach —— 函数式风格 =====
arr.forEach(function(item, index) {
  console.log(item); // a, b, c
});
// 优点：简洁
// 缺点：不能用break/continue/return跳出；只能用于数组

// ===== for...in —— 遍历"键" =====
for (var key in arr) {
  console.log(key, arr[key]);
}
// 输出:
// "0" "a"
// "1" "b"
// "2" "c"
// "foo" "额外属性" —— 糟糕！把自定义属性也遍历出来了！
// 还会遍历到原型链上的可枚举属性
// for...in的key是字符串，不是数字

// ===== ES6：for...of —— 遍历"值" =====
for (const item of arr) {
  console.log(item); // a, b, c
}
// 优点：只遍历元素值，不包括额外属性；支持break/continue；不限于数组
```

| 特性 | for | forEach | for...in | for...of |
|------|-----|---------|----------|----------|
| 遍历目标 | 索引 | 数组元素 | **可枚举属性名** | **可迭代对象的值** |
| break/continue | 支持 | **不支持** | 支持 | 支持 |
| 遍历顺序 | 手动控制 | 按索引 | 不保证 | 按迭代器顺序 |
| 额外属性 | 不会遍历 | 不会遍历 | **会遍历到！** | 不会遍历 |
| 适用对象 | 数组/类数组 | 数组 | 对象 | **所有可迭代对象** |
| 异步中使用 | 可以 | 容易踩坑 | 可以 | 可以（配合async） |

### 7.4.2 for...of遍历各种数据结构

```javascript
// --- 数组 ---
const arr = [10, 20, 30];
for (const value of arr) {
  console.log(value); // 10, 20, 30
}

// 用entries()同时获取索引和值
for (const [index, value] of arr.entries()) {
  console.log(`${index}: ${value}`); // "0: 10", "1: 20", "2: 30"
}

// --- 字符串 ---
for (const char of 'Hello') {
  console.log(char); // H, e, l, l, o
}
// 注意：for...in遍历字符串会给出"0","1","2","3","4"

// --- Map ---
const map = new Map([['a', 1], ['b', 2]]);
for (const [key, value] of map) {
  console.log(`${key} = ${value}`); // "a = 1", "b = 2"
}

// --- Set ---
const set = new Set([1, 2, 3]);
for (const value of set) {
  console.log(value); // 1, 2, 3
}

// --- 类数组对象（arguments/NodeList）---
function test() {
  for (const arg of arguments) {
    console.log(arg);
  }
}
test('x', 'y', 'z'); // x, y, z

// --- break和continue照样用 ---
for (const num of [1, 2, 3, 4, 5]) {
  if (num === 3) break;      // 遇到3就跳出
  console.log(num);           // 1, 2
}
```

### 7.4.3 与解构赋值结合

```javascript
const users = [
  { id: 1, name: '张三' },
  { id: 2, name: '李四' },
  { id: 3, name: '王五' }
];

// for...of + 解构 = 优雅！
for (const { id, name } of users) {
  console.log(`用户${id}: ${name}`);
}
// 输出:
// 用户1: 张三
// 用户2: 李四
// 用户3: 王五

// 遍历Map时解构
const scores = new Map([
  ['语文', 90],
  ['数学', 95],
  ['英语', 88]
]);

for (const [subject, score] of scores) {
  console.log(`${subject}: ${score}分`);
}
```

---

## 7.5 迭代器（Iterator）与可迭代协议

### 7.5.1 什么是迭代器？

迭代器就像一个**自动售货机的出货口**——你每次按按钮（调用`next()`），它就吐出一个商品（值），直到货物卖完（`done: true`）。

在JavaScript中，迭代器是一个**遵守特定接口的对象**：

```javascript
// 迭代器的基本结构
const iterator = {
  next() {
    return {
      value: /* 当前值 */,    // 当前元素的值
      done: /* true/false */  // false=还有值，true=迭代完了
    };
  }
};
```

### 7.5.2 手动创建迭代器

```javascript
// ===== ES5：手动写一个"范围"迭代器 =====
function createRangeIterator(start, end) {
  var current = start;
  return {
    next: function() {
      if (current <= end) {
        return { value: current++, done: false };
      }
      return { value: undefined, done: true };
    }
  };
}

var iter = createRangeIterator(1, 3);
console.log(iter.next()); // { value: 1, done: false }
console.log(iter.next()); // { value: 2, done: false }
console.log(iter.next()); // { value: 3, done: false }
console.log(iter.next()); // { value: undefined, done: true }

// ===== ES6：同样的迭代器，语法更简洁 =====
function createRangeIteratorES6(start, end) {
  let current = start;
  return {
    next() {
      return current <= end
        ? { value: current++, done: false }
        : { done: true };  // value可省略，默认为undefined
    }
  };
}
```

### 7.5.3 可迭代协议（Iterable Protocol）

一个对象要成为**可迭代对象**（可以用`for...of`遍历），必须实现`[Symbol.iterator]`方法，返回一个迭代器。

```javascript
// ===== 让一个对象可以被for...of遍历 =====

const classroom = {
  students: ['张三', '李四', '王五'],

  // 实现可迭代协议
  [Symbol.iterator]() {
    let index = 0;
    const students = this.students;

    return {
      next() {
        if (index < students.length) {
          return { value: students[index++], done: false };
        }
        return { done: true };
      }
    };
  }
};

// 现在可以用for...of遍历了！
for (const student of classroom) {
  console.log(student); // 张三, 李四, 王五
}

// 也可以用展开运算符
console.log([...classroom]); // ["张三", "李四", "王五"]

// 也可以用解构
const [first, ...rest] = classroom;
console.log(first); // "张三"
console.log(rest);  // ["李四", "王五"]
```

### 7.5.4 生成器函数：更优雅的迭代器写法

ES6的生成器函数（`function*`）让写迭代器变得超级简单：

```javascript
// ===== 传统迭代器写法 =====
const obj1 = {
  [Symbol.iterator]() {
    let i = 0;
    return {
      next() {
        if (i < 3) return { value: i++, done: false };
        return { done: true };
      }
    };
  }
};

// ===== 生成器函数写法 —— 优雅太多了！ =====
const obj2 = {
  *[Symbol.iterator]() {   // function* 简写为 *[Symbol.iterator]
    yield 1;
    yield 2;
    yield 3;
  }
};

console.log([...obj2]); // [1, 2, 3]

// 生成器函数会自动创建迭代器对象，yield的值就是next().value

// 甚至可以这样写：yield*
const obj3 = {
  *[Symbol.iterator]() {
    yield* [1, 2, 3];  // yield* 委托给另一个可迭代对象
    yield 4;
    yield 5;
  }
};
console.log([...obj3]); // [1, 2, 3, 4, 5]
```

### 7.5.5 哪些内置对象是可迭代的？

```javascript
// ES6内置的可迭代对象：
const iterables = [
  [1, 2, 3],                          // 数组
  'hello',                            // 字符串
  new Map([['a', 1]]),               // Map
  new Set([1, 2, 3]),                // Set
  new Int8Array([1, 2, 3]),          // TypedArray
  arguments                           // 函数参数（类数组）
];

// 检验方法：检查是否有Symbol.iterator方法
for (const item of iterables) {
  console.log(typeof item[Symbol.iterator] === 'function'); // 全是true
}

// 注意：普通对象{}默认不是可迭代的！
const plainObj = { a: 1, b: 2 };
// for (const x of plainObj) {} // TypeError: plainObj is not iterable

// 对象的遍历还是用for...in或Object.entries()
for (const [key, value] of Object.entries(plainObj)) {
  console.log(`${key}: ${value}`); // "a: 1", "b: 2"
}
```

---

## 7.6 函数的细节改进

### 7.6.1 函数名的name属性

ES6为函数添加了标准的`name`属性，让调试和元编程更方便。

```javascript
// ===== ES5：获取函数名很麻烦 =====
function myFunc() {}
// 没有标准方法获取函数名，只能解析toString()
var funcName = myFunc.toString().match(/function\s+([^\s(]+)/)?.[1];
console.log(funcName); // "myFunc" —— 不靠谱！

// ===== ES6：每个函数都有name属性 =====
function doSomething() {}
console.log(doSomething.name); // "doSomething"

// 匿名函数赋值后，name从变量名推断
const myMethod = function() {};
console.log(myMethod.name); // "myMethod" —— ES6的魔法！

// 但作为回调时可能还是匿名
setTimeout(function() {}, 100);
// 这个回调在堆栈追踪中显示为"anonymous"

// --- 各种函数定义的name属性 ---

// 1. 函数声明
function declaredFunc() {}
console.log(declaredFunc.name); // "declaredFunc"

// 2. 函数表达式
const expressedFunc = function namedFunc() {};
console.log(expressedFunc.name); // "namedFunc" —— 显示表达式的名字

const anonymousFunc = function() {};
console.log(anonymousFunc.name); // "anonymousFunc" —— 从变量名推断

// 3. 箭头函数
const arrowFunc = () => {};
console.log(arrowFunc.name); // "arrowFunc"

// 4. 对象方法
const obj = {
  regularMethod() {},    // ES6简写
  arrowMethod: () => {},
  [Symbol('sym')]() {}   // Symbol属性名
};
console.log(obj.regularMethod.name); // "regularMethod"
console.log(obj.arrowMethod.name);   // "arrowMethod"

// 5. class中的方法
class MyClass {
  myMethod() {}
  static staticMethod() {}
}
const instance = new MyClass();
console.log(instance.myMethod.name);   // "myMethod"
console.log(MyClass.staticMethod.name); // "staticMethod"

// 6. getter/setter
const descriptor = {
  get value() { return 42; },
  set value(v) {}
};
// getter和setter的name前缀是"get "和"set "
const getter = Object.getOwnPropertyDescriptor(descriptor, 'value').get;
console.log(getter.name); // "get value"

// 7. bind后的函数
const boundFunc = function original() {}.bind(null);
console.log(boundFunc.name); // "bound original"

// 8. 构造函数
console.log((new Function()).name); // "anonymous"
```

### 7.6.2 默认参数对arguments的影响

```javascript
// ===== ES5：arguments和形参总是联动 =====
function es5Func(a, b) {
  console.log(arguments[0], a); // 永远一样
  a = 100; // 修改a
  console.log(arguments[0]);    // 也变成100（严格模式下不联动）
  return a + b;
}

// ===== ES6：默认参数改变了arguments的行为 =====
// 在ES6中，如果一个函数使用了默认参数：
// 1. 它自动进入"严格模式"的arguments行为（arguments和形参不联动）
// 2. arguments对象不会包含超出形参数量的值

function es6Func(a = 1, b = 2) {
  console.log(arguments);       // 只包含实际传入的参数
  console.log(a, b);            // 包含默认值填充后的值

  a = 999;
  console.log(arguments[0]);    // 不变！arguments和形参解耦了
}

es6Func();           // arguments: {}        a:1, b:2
es6Func(10);         // arguments: {0:10}    a:10, b:2
es6Func(10, 20);     // arguments: {0:10,1:20} a:10, b:20
es6Func(10, 20, 30); // arguments: {0:10,1:20} a:10, b:20（多余的不在arguments里）

// --- 对比：无默认参数的函数（旧行为） ---
function oldStyle(a, b) {
  a = 999;
  console.log(arguments[0]); // 999 —— 联动修改了
}
oldStyle(1, 2); // arguments[0] 变成 999

// --- rest参数时arguments完全不同 ---
function withRest(a, ...rest) {
  console.log(arguments); // {0: 1, 1: 2, 2: 3}
  console.log(rest);      // [2, 3] —— rest只包含多余的
}
withRest(1, 2, 3);
```

### 7.6.3 函数参数的尾逗号

```javascript
// ES2017允许在函数参数列表的最后加一个逗号
// 这在多行参数时特别有用，减少diff的噪音

function setupApp(
  config,
  middleware,
  routes,     // ← 这里可以加逗号！方便后续添加参数
) {
  // ...
}

// 函数调用也支持
setupApp(
  { port: 3000 },
  [logger, cors],
  userRoutes,  // ← 尾逗号
);

// 同样适用于数组和对象
const arr = [
  1,
  2,
  3,  // ← 尾逗号
];

const obj = {
  a: 1,
  b: 2,  // ← 尾逗号
};

// 好处：在Git diff中添加新行时，只显示新增的行，不会连带修改上一行
```

---

## 7.7 本章小结

```javascript
// ===== 本章核心知识点回顾 =====

// 1. Map —— 专业级键值对存储
const map = new Map([['key', 'value']]);
map.set(anyKey, anyValue);  // 键可以是任意类型
map.get(anyKey);            // 取值
map.has(anyKey);            // 检查
map.delete(anyKey);         // 删除
map.size;                   // 大小

// 2. Set —— 自动去重集合
const set = new Set([1, 2, 2, 3]);
set.add(value);     // 添加（重复自动忽略）
set.has(value);     // 检查是否存在
[...set];           // 转数组

// 3. Symbol —— 独一无二的标识符
const sym = Symbol('描述');
const obj = { [sym]: '私有数据' }; // 不会跟任何其他属性冲突

// 4. for...of —— 遍历值而非键
for (const value of iterable) { /* ... */ }

// 5. 可迭代协议
// 对象实现 [Symbol.iterator]() 方法即可被for...of遍历

// 6. 函数细节
// .name属性：获取函数名
// 默认参数：arguments和形参解耦
// 尾逗号：减少版本控制diff噪音
```

---
---

# 附录

> **附录导读**：恭喜你读完了全部七章内容！本附录是你学习ES6的"工具箱"——包含一份可以贴在显示器旁边的速查表、一张详细的ES5 vs ES6对比表、一条从新手到高手的学习路线图，以及经过筛选的优质学习资源。建议收藏本附录，随时查阅。

---

## 附录A：ES6特性速查表（Quick Reference）

### A.1 变量声明

| 特性 | 语法 | 说明 |
|------|------|------|
| `let` | `let x = 1;` | 块级作用域，可重新赋值，不可重复声明 |
| `const` | `const x = 1;` | 块级作用域，不可重新赋值，不可重复声明 |
| 暂时性死区 | `let x = x; // 报错` | 声明前访问会`ReferenceError` |
| 常量对象 | `const obj = {}; obj.a=1; // OK` | `const`冻结的是绑定，不是值 |

### A.2 箭头函数

| 特性 | 语法 | 说明 |
|------|------|------|
| 基本语法 | `const f = x => x * 2;` | 单参数可省略括号 |
| 多参数 | `const add = (a, b) => a + b;` | 多参数需括号 |
| 多行体 | `(x) => { return x * 2; }` | 多行需花括号和return |
| 返回对象 | `x => ({ a: x })` | 返回对象需用括号包裹 |
| this绑定 | 继承外层this | 不能用作构造函数，没有自己的this |

### A.3 模板字符串

| 特性 | 语法 | 说明 |
|------|------|------|
| 基本用法 | `` `Hello ${name}` `` | 用`${}`嵌入表达式 |
| 多行 | `` `第1行\n第2行` `` | 保留换行和缩进 |
| 标签模板 | `` tag`Hello ${name}` `` | 第一个参数是字符串数组，后续是插值 |

### A.4 解构赋值

| 特性 | 语法 | 说明 |
|------|------|------|
| 数组解构 | `const [a, b] = arr;` | 按位置解构 |
| 对象解构 | `const {a, b} = obj;` | 按属性名解构 |
| 嵌套解构 | `const {a: {b}} = obj;` | 支持嵌套结构 |
| 默认值 | `const {a = 1} = obj;` | 解构时设默认值 |
| 重命名 | `const {a: alias} = obj;` | 解构时重命名变量 |
| 剩余 | `const [a, ...rest] = arr;` | 用rest收集剩余元素 |
| 函数参数 | `fn({a, b})` | 直接解构形参 |

### A.5 展开/剩余运算符

| 特性 | 语法 | 说明 |
|------|------|------|
| 数组展开 | `[...arr1, ...arr2]` | 展开数组元素 |
| 对象展开 | `{...obj1, ...obj2}` | 展开对象属性（ES2018） |
| 函数调用 | `fn(...args)` | 数组展开为参数 |
| 剩余参数 | `function(a, ...rest)` | 收集多余参数为数组 |

### A.6 类（Class）

| 特性 | 语法 | 说明 |
|------|------|------|
| 类声明 | `class Foo {}` | 非提升，严格模式 |
| 构造函数 | `constructor() {}` | 每个类一个 |
| 实例方法 | `method() {}` | 定义在原型上 |
| 静态方法 | `static method() {}` | 定义在类上 |
| 继承 | `class B extends A {}` | 单继承 |
| super调用 | `super(); super.method()` | 调用父类构造/方法 |
| getter/setter | `get name() {}` | 属性访问器 |
| 类字段 | `name = 'value';` | 类字段声明（ES2022） |
| 私有字段 | `#count = 0;` | 真正的私有属性（ES2022） |

### A.7 模块（Module）

| 特性 | 语法 | 说明 |
|------|------|------|
| 导出 | `export const x = 1;` | 命名导出 |
| 默认导出 | `export default x;` | 一个模块只有一个 |
| 导入 | `import { x } from './mod';` | 命名导入 |
| 默认导入 | `import x from './mod';` | 导入默认导出 |
| 全部导入 | `import * as mod from './mod';` | 导入为命名空间 |
| 重命名 | `import { x as y } from './mod';` | 导入时重命名 |
| 混合导入 | `import x, { y } from './mod';` | 同时导入默认和命名 |
| 动态导入 | `const mod = await import('./mod');` | 运行时异步导入 |

### A.8 Promise

| 特性 | 语法 | 说明 |
|------|------|------|
| 创建 | `new Promise((resolve, reject) => {})` | 执行器函数 |
| then | `.then(val => {}, err => {})` | 成功/失败回调 |
| catch | `.catch(err => {})` | 错误处理 |
| finally | `.finally(() => {})` | 无论成败都执行 |
| 静态方法 | `Promise.all([...])` | 全部完成 |
| | `Promise.race([...])` | 竞争，最快的一个 |
| | `Promise.allSettled([...])` | 全部结束（不论成败） |
| | `Promise.any([...])` | 任意一个成功 |
| | `Promise.resolve(val)` | 创建已解决Promise |
| | `Promise.reject(err)` | 创建已拒绝Promise |

### A.9 async/await

| 特性 | 语法 | 说明 |
|------|------|------|
| async函数 | `async function() {}` | 总是返回Promise |
| await | `const val = await promise;` | 暂停等待Promise解决 |
| 错误处理 | `try { await p; } catch(e) {}` | 用try/catch处理错误 |
| 并行执行 | `await Promise.all([a, b])` | 并行等待多个Promise |
| 循环中await | `for await (x of asyncIter)` | 异步迭代 |

### A.10 新数据结构

| 特性 | 语法 | 说明 |
|------|------|------|
| Map | `new Map([[k, v]])` | 键值对，键可为任意类型 |
| Map.set/get | `map.set(k, v); map.get(k)` | 存取 |
| Map遍历 | `for([k, v] of map)` | 保证插入顺序 |
| Set | `new Set([1, 2, 2])` | 唯一值集合，自动去重 |
| Set操作 | `set.add(v); set.has(v)` | 添加/检查 |
| WeakMap | `new WeakMap()` | 弱引用键，适合私有数据 |
| WeakSet | `new WeakSet()` | 弱引用对象集合 |

### A.11 Symbol

| 特性 | 语法 | 说明 |
|------|------|------|
| 创建 | `const s = Symbol('desc');` | 每次创建都不同 |
| 对象属性 | `obj[s] = 'value';` | 不会跟任何属性冲突 |
| 不可枚举 | `Object.keys()`不返回 | 需用`getOwnPropertySymbols` |
| 全局注册 | `Symbol.for('key')` | 全局共享的Symbol |
| 反向查找 | `Symbol.keyFor(sym)` | 获取全局Symbol的key |
| 内置Symbol | `Symbol.iterator`等 | 控制对象内部行为 |

### A.12 迭代

| 特性 | 语法 | 说明 |
|------|------|------|
| for...of | `for (const x of iterable)` | 遍历可迭代对象的值 |
| 可迭代协议 | `[Symbol.iterator]()` | 实现此方法即可迭代 |
| 生成器 | `function* gen() { yield 1; }` | 简化迭代器创建 |
| yield* | `yield* [1, 2, 3];` | 委托给另一个可迭代对象 |

### A.13 函数增强

| 特性 | 语法 | 说明 |
|------|------|------|
| 默认参数 | `function(a = 1) {}` | 参数默认值 |
| 解构参数 | `function({a, b}) {}` | 解构传入的对象 |
| name属性 | `func.name` | 获取函数名 |
| 尾逗号 | `fn(a, b,)` | 参数尾逗号（ES2017） |

### A.14 对象增强

| 特性 | 语法 | 说明 |
|------|------|------|
| 简写属性 | `{a, b}` | 等价于`{a: a, b: b}` |
| 简写方法 | `{foo() {}}` | 等价于`{foo: function() {}}` |
| 计算属性 | `{[key]: value}` | 用表达式作为属性名 |
| super关键字 | `super.method()` | 在对象方法中调用原型方法 |
| Object.assign | `Object.assign({}, a, b)` | 对象浅拷贝/合并 |
| Object.is | `Object.is(NaN, NaN)` | 严格相等（+0 !== -0） |

---

## 附录B：ES5 vs ES6写法对比表

> 左列为ES5（传统写法），右列为ES6+（现代写法）。建议熟记这张表，在实际编码中逐步从左侧过渡到右侧。

### B.1 变量与常量

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| 变量声明 | `var count = 0;` | `let count = 0;` |
| 常量声明 | `var PI = 3.14159; // 只是约定` | `const PI = 3.14159; // 真正不可变` |
| 块级作用域 | `var i = 0; for(...) { var i = 1; } // i变成1` | `let i = 0; for(...) { let i = 1; } // 互不影响` |
| 循环变量 | `for (var i = 0; i < 3; i++) {} console.log(i); // 3` | `for (let i = 0; i < 3; i++) {} console.log(i); // ReferenceError` |

### B.2 函数

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| 简单函数 | `var double = function(x) { return x * 2; };` | `const double = x => x * 2;` |
| 多参数函数 | `var add = function(a, b) { return a + b; };` | `const add = (a, b) => a + b;` |
| 多行函数 | `var greet = function(name) { var msg = 'Hi ' + name; return msg; };` | `const greet = name => { const msg = \`Hi ${name}\`; return msg; };` |
| 回调函数 | `arr.map(function(x) { return x * 2; });` | `arr.map(x => x * 2);` |
| this绑定 | `var self = this; setTimeout(function() { self.doSomething(); }, 100);` | `setTimeout(() => this.doSomething(), 100);` |
| 默认参数 | `function greet(name) { name = name || 'Guest'; return 'Hi ' + name; }` | `const greet = (name = 'Guest') => \`Hi ${name}\`;` |
| 剩余参数 | `function sum() { var args = Array.prototype.slice.call(arguments); return args.reduce(function(a, b) { return a + b; }, 0); }` | `const sum = (...args) => args.reduce((a, b) => a + b, 0);` |
| 参数解构 | `function greet(options) { var name = options.name; var age = options.age; }` | `const greet = ({ name, age }) => { };` |

### B.3 字符串

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| 字符串拼接 | `'Hello, ' + name + '! You are ' + age + ' years old.'` | `` `Hello, ${name}! You are ${age} years old.` `` |
| 多行字符串 | `'First line\\n' + 'Second line\\n' + 'Third line'` | `` `First line\nSecond line\nThird line` `` |
| 包含引号的字符串 | "He said \"Hello\"" | `` `He said "Hello"` `` |
| 原始字符串 | 无原生支持 | `` String.raw`C:\\Users\\Name` `` |

### B.4 数组

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| 数组遍历 | `for (var i = 0; i < arr.length; i++) { console.log(arr[i]); }` | `for (const item of arr) { console.log(item); }` |
| 数组映射 | `arr.map(function(x) { return x * 2; });` | `arr.map(x => x * 2);` |
| 数组过滤 | `arr.filter(function(x) { return x > 0; });` | `arr.filter(x => x > 0);` |
| 查找元素 | `arr.filter(function(x) { return x.id === 1; })[0];` | `arr.find(x => x.id === 1);` |
| 数组去重 | `arr.filter(function(item, index, self) { return self.indexOf(item) === index; });` | `[...new Set(arr)];` |
| 数组合并 | `arr1.concat(arr2).concat(arr3);` | `[...arr1, ...arr2, ...arr3];` |
| 数组展开传参 | `fn.apply(null, args);` | `fn(...args);` |
| 判断包含 | `arr.indexOf(item) !== -1;` | `arr.includes(item);` |
| Array.from | `Array.prototype.slice.call(nodeList);` | `Array.from(nodeList);` |

### B.5 对象

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| 属性简写 | `{ name: name, age: age }` | `{ name, age }` |
| 方法简写 | `{ sayHi: function() { } }` | `{ sayHi() { } }` |
| 计算属性 | `var obj = {}; obj[key] = value;` | `{ [key]: value }` |
| 对象合并 | `var merged = Object.assign({}, a, b);` | `const merged = { ...a, ...b };` |
| 对象浅拷贝 | `var copy = Object.assign({}, obj);` | `const copy = { ...obj };` |
| 对象转数组 | `Object.keys(obj).map(function(k) { return [k, obj[k]]; });` | `Object.entries(obj);` |
| 设置原型 | `Object.create(parent);` | `{ __proto__: parent }` 或 class extends |

### B.6 解构

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| 数组解构 | `var first = arr[0], second = arr[1];` | `const [first, second] = arr;` |
| 对象解构 | `var name = person.name, age = person.age;` | `const { name, age } = person;` |
| 深层解构 | `var street = user.address.street;` | `const { address: { street } } = user;` |
| 解构+重命名 | `var n = person.name;` | `const { name: n } = person;` |
| 解构+默认值 | `var role = user.role || 'user';` | `const { role = 'user' } = user;` |
| 交换变量 | `var tmp = a; a = b; b = tmp;` | `[a, b] = [b, a];` |
| 跳过元素 | `var third = arr[2];` | `const [,, third] = arr;` |

### B.7 类与继承

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| 类声明 | `function Animal(name) { this.name = name; }` | `class Animal { constructor(name) { this.name = name; } }` |
| 实例方法 | `Animal.prototype.speak = function() { };` | `class Animal { speak() { } }` |
| 静态方法 | `Animal.isAnimal = function(obj) { };` | `class Animal { static isAnimal(obj) { } }` |
| 继承 | `function Dog(name) { Animal.call(this, name); } Dog.prototype = Object.create(Animal.prototype);` | `class Dog extends Animal { constructor(name) { super(name); } }` |
| 调用父方法 | `Animal.prototype.speak.call(this);` | `super.speak();` |
| 私有属性（传统） | 用闭包或`_prefix`约定 | `class A { #count = 0; } // 真正私有` |

### B.8 模块

| 场景 | ES5/AMD/CommonJS | ES6 Module |
|------|-----------------|------------|
| 导出 | `module.exports = foo; exports.bar = bar;` | `export default foo; export { bar };` |
| 导入 | `var foo = require('./foo');` | `import foo from './foo';` |
| 命名导入 | `var bar = require('./foo').bar;` | `import { bar } from './foo';` |
| 条件导入 | `if (condition) { require('./extra'); }` | `if (condition) { await import('./extra'); }` |

### B.9 异步编程

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| 回调嵌套 | `loadData(function(a) { loadMore(a, function(b) { loadMore(b, function(c) { }); }); });` | `const a = await loadData(); const b = await loadMore(a); const c = await loadMore(b);` |
| Promise链 | `fetch('/api').then(function(r) { return r.json(); }).then(function(d) { console.log(d); });` | `const r = await fetch('/api'); const d = await r.json(); console.log(d);` |
| 错误处理 | `doAsync(function(err, data) { if (err) { handle(err); return; } });` | `try { const data = await doAsync(); } catch (err) { handle(err); }` |
| 并行执行 | `async.parallel([fn1, fn2], function(err, results) { });` | `const [r1, r2] = await Promise.all([fn1(), fn2()]);` |
| Promise创建 | `new Promise(function(resolve, reject) { if (ok) resolve(val); else reject(err); });` | `new Promise((resolve, reject) => { if (ok) resolve(val); else reject(err); });` |

### B.10 新数据结构

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| Map存储 | `var map = {}; map[key] = value; // key被转字符串` | `const map = new Map(); map.set(key, value); // key保持原类型` |
| 检查键存在 | `if (map[key] !== undefined)` | `if (map.has(key))` |
| 获取大小 | `Object.keys(map).length` | `map.size` |
| 数组去重 | `arr.filter(function(v, i, s) { return s.indexOf(v) === i; });` | `[...new Set(arr)];` |
| 遍历Map | `Object.keys(obj).forEach(function(k) { });` | `for (const [k, v] of map) { }` |

### B.11 Symbol与迭代

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| 唯一属性名 | `var KEY = '__mylib_key_' + Math.random();` | `const KEY = Symbol('mylib_key');` |
| 自定义迭代 | 不可行，无原生支持 | `*[Symbol.iterator]() { yield 1; yield 2; }` |
| 遍历可迭代对象 | `var it = arr[Symbol.iterator](); var r; while(!(r = it.next()).done) { console.log(r.value); }` | `for (const x of arr) { console.log(x); }` |

### B.12 其他语法糖

| 场景 | ES5（传统写法） | ES6+（现代写法） |
|------|----------------|-----------------|
| 函数name | `func.toString().match(/function\s+([^\s(]+)/)[1]` | `func.name` |
| 指数运算 | `Math.pow(2, 10);` | `2 ** 10; // ES2016` |
| 空值合并 | `var val = x != null ? x : defaultVal;` | `const val = x ?? defaultVal; // ES2020` |
| 可选链 | `var street = user && user.address && user.address.street;` | `const street = user?.address?.street; // ES2020` |
| 逻辑赋值 | `a = a || b;` | `a ??= b; a ||= b; a &&= b; // ES2021` |
| Promise.allSettled | 无原生支持 | `Promise.allSettled([p1, p2]); // ES2020` |
| 动态导入 | `require(moduleName);` | `await import(moduleName); // ES2020` |
| BigInt | 超出Number.MAX_SAFE_INTEGER失真 | `const big = 9007199254740993n; // ES2020` |
| 顶层await | 必须在async函数内 | `const data = await fetch('/api'); // ES2022` |

---

## 附录C：ES6学习路线图

### 阶段一：基础入门（1-2周）

> **目标**：掌握ES6最常用的语法，能看懂和编写现代JavaScript代码。

```
第1周
├── let 和 const（替代var）
├── 箭头函数（=>）
├── 模板字符串（`${}`）
├── 默认参数和剩余参数
└── 展开运算符（...）

第2周
├── 解构赋值（数组和对象）
├── 对象简写语法（简写属性和方法）
├── 类（class）基础
├── 模块（import/export）基础
└── for...of 循环
```

**学习建议**：
- 每天学习1-2个特性
- 每个特性都要动手写代码练习
- 尝试把之前用ES5写的代码改成ES6

### 阶段二：进阶核心（2-3周）

> **目标**：掌握异步编程和新数据结构，能处理复杂场景。

```
第3周
├── Promise 深入（then/catch/finally）
├── Promise 静态方法（all/race等）
├── async/await 基础
└── async/await 错误处理

第4周
├── Map 和 Set 数据结构
├── Symbol 类型和应用
├── 迭代器与生成器（Iterator/Generator）
└── 类的继承和super

第5周
├── 模块系统进阶（动态导入、循环依赖）
├── Proxy 和 Reflect（ES6元编程）
└── 综合实战项目
```

**学习建议**：
- 重点理解异步编程的执行流程
- 用Promise和async/await重写回调代码
- 尝试用Map/Set解决实际问题

### 阶段三：深入精通（持续学习）

> **目标**：理解ES6+底层机制，能参与框架开发和代码库设计。

```
持续学习
├── ES2016-ES2024新特性
│   ├── 指数运算符（**）
│   ├── Array.prototype.includes
│   ├── Object.entries/Object.values
│   ├── async迭代（for await...of）
│   ├── 可选链（?.）
│   ├── 空值合并（??）
│   ├── Promise.allSettled
│   ├── 类私有字段（#）
│   ├── 顶层await
│   └── 数组方法（at/toSorted等）
├── 底层原理
│   ├── 迭代器协议深入
│   ├── Promise实现原理
│   ├── 生成器与协程
│   └── V8引擎优化
└── 工程化
    ├── Babel转译原理
    ├── Tree Shaking
    └── Polyfill策略
```

### 学习检验清单

用这份清单检验你的学习成果，全部打勾说明你已经掌握了ES6：

- [ ] 能用`let/const`替代所有`var`，不出错
- [ ] 能熟练编写箭头函数，知道什么时候不该用
- [ ] 能用模板字符串写出清晰的多行文本
- [ ] 能一眼看出解构赋值的写法，能熟练运用
- [ ] 能用`...`运算符完成展开和收集操作
- [ ] 能用`class`定义类，理解继承和`super`
- [ ] 能用`import/export`组织代码
- [ ] 能用`Promise`和`async/await`处理异步
- [ ] 知道什么时候用`Map/Set`替代`Object/Array`
- [ ] 理解`Symbol`的作用，知道应用场景
- [ ] 能用`for...of`遍历各种数据结构
- [ ] 了解迭代器的基本概念

---

## 附录D：推荐学习资源

### 官方文档与标准

| 资源 | 链接 | 说明 |
|------|------|------|
| MDN Web Docs | developer.mozilla.org | **最权威的中文参考**，每个特性都有详细文档和浏览器兼容性 |
| ECMAScript规范 | tc39.es/ecma262 | 语言标准原文，适合深入理解细节 |
| TC39提案 | github.com/tc39/proposals | 查看正在讨论和制定中的新特性 |
| Can I Use | caniuse.com | 查询各特性的浏览器支持情况 |

### 在线学习平台

| 资源 | 说明 |
|------|------|
| JavaScript.info (现代教程) | 从基础到高级的完整JS教程，ES6+覆盖全面 |
| 阮一峰 ES6入门教程 | 中文ES6入门经典，适合系统学习 |
| freeCodeCamp | 免费交互式编程练习 |
| Egghead.io | 大量短视频教程，有很多前沿内容 |

### 推荐书籍

| 书名 | 作者 | 适合阶段 |
|------|------|------|
| 《JavaScript高级程序设计》（第4版） | Matt Frisbie | 基础-进阶，红宝书最新版已全面覆盖ES6+ |
| 《深入理解ES6》 | Nicholas C. Zakas | 进阶，深入讲解每个特性的设计原因 |
| 《JavaScript忍者秘籍》（第2版） | John Resig等 | 进阶，讲解函数、闭包、原型等核心概念 |
| 《你不知道的JavaScript》 | Kyle Simpson | 深入，理解JS底层机制 |
| 《JavaScript异步编程》 |  | 进阶，专讲Promise和异步模式 |

### 实战练习资源

| 资源 | 说明 |
|------|------|
| ES6 Kata | 专门针对ES6新特性的编程练习 |
| Codewars | 用ES6+完成各种算法挑战 |
| LeetCode | 用现代JS刷算法题 |
| GitHub优秀项目 | 阅读使用ES6+的开源项目源码 |

### 开发工具

| 工具 | 用途 |
|------|------|
| Babel | ES6+转ES5，让旧浏览器也能运行 |
| ESLint + Prettier | 代码规范和格式化 |
| VS Code | 编辑器，配合ES6+代码片段 |
| Node.js 14+ | 运行环境，原生支持绝大部分ES6+特性 |

### 学习社区

| 社区 | 说明 |
|------|------|
| Stack Overflow | 编程问题问答 |
| GitHub Discussions | 开源项目讨论 |
| 掘金 | 中文技术社区，有很多ES6相关文章 |
| 知乎/segmentfault | 中文技术问答 |

---

> **写在最后**：ES6不是终点，而是一个起点。从2015年ES6发布以来，JavaScript每年都有新特性加入（ES2016、ES2017...ES2024）。掌握ES6的核心概念后，每年新增的特性都只是在这个基础上的"增量更新"。保持好奇心，多写代码，多看优秀源码，你的JavaScript之路会越走越宽广。
>
> **祝编码愉快！**

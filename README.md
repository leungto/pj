
### 后端

运行前端：（进入前端frontend里）

```
npm run dev
```

运行后端：（进入后端myback里）

```
python manage.py runserver localhost:3001
```

前端运行在localhost:3000上，向3001端口发请求

目前实现了用户注册和登录

以下是前端仓库的readme，前端仓库的后端是用的flaskapi建的，我们的仓库在myback里
-------------
后端：

推荐使用PDM来管理Python包环境

安装，参考：[https://pdm-project.org/latest/](https://pdm-project.org/latest/)

配置环境（在backend路径下）：

```bash
pdm install
```

启动（在backend路径下）：

```bash
fastapi dev --port 3001
```

我这里实现的是用SQLite的数据库，这个不需要配置额外的环境，而且vscode装一个插件可以直接看数据库内内容。

-------------

前端：

安装：[https://nodejs.org/zh-cn/download](https://nodejs.org/zh-cn/download)

我这里用的是 v24.0.2 using nvm with npm

启动 (在frontend路径下)：

```bash
npm run dev
```

-----------------

tests:
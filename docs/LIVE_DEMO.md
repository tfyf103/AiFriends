# AiFriends Live Demo Verification / 在线体验验证

🌐 **Live deployment / 实际部署：** <https://app8056.acapp.acwing.com.cn/>

This document records how the real screenshots in this repository were obtained. / 本文记录仓库中真实线上截图的采集方式。

## Verification / 验证方式

On **2026-08-11**, a GitHub-hosted `ubuntu-24.04` runner used **Playwright 1.55 + Chromium 140** to visit the production deployment from an independent public network.

2026-08-11，项目使用 GitHub-hosted `ubuntu-24.04` runner，通过 **Playwright 1.55 + Chromium 140** 从独立公网环境访问真实线上部署。

The run was intentionally read-only / 本次体验刻意保持只读：

- no test account registration / 未注册测试账号；
- no Character creation / 未创建角色；
- no Friend creation or chat messages / 未创建 Friend 或发送聊天消息；
- no production-data mutation / 未修改生产数据。

## Verified routes / 已验证页面

| Route | HTTP | Observation / 实际观察 |
|---|---:|---|
| `/` | 200 | Public Character discovery / 公开角色发现 |
| `/user/account/login` | 200 | Login form / 登录表单 |
| `/user/account/register` | 200 | Registration form / 注册表单 |
| `/user/space/6` | 200 | Public user space and Character content / 公开用户空间与角色内容 |

## Real screenshots / 真实截图

### Homepage / 首页

![Live homepage](./assets/live-demo/homepage.png)

### Login / 登录

![Live login](./assets/live-demo/login.png)

### Register / 注册

![Live register](./assets/live-demo/register.png)

### Public user space / 公开用户空间

![Live public user space](./assets/live-demo/public-profile.png)

## Scope note / 范围说明

These images are point-in-time production snapshots, not generated mockups. Public Characters, profile text, images, and deployed frontend assets can change after capture.

这些图片是某一时刻的真实线上快照，不是生成图或设计稿。公开角色、用户资料、图片和线上部署版本之后都可能变化。

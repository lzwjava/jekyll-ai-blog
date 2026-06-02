---
audio: false
generated: true
lang: zh
layout: post
title: 修复YouTube-dl机器人验证错误
translated: true
type: note
---

youtube-dl 出现的“请登录以确认您不是机器人”错误通常是因为 YouTube 屏蔽了请求，常见原因包括 IP 限制、VPN 使用或缺乏身份验证。以下是解决问题的步骤，从最简单的方案开始：

1. **更新 youtube-dl**：
   - 该错误可能源于 youtube-dl 版本过时，因为 YouTube 会频繁更新其系统。通过以下命令更新至最新版本：

     ```bash
     sudo youtube-dl -U
     ```

     若通过 pip 安装则使用：

     ```bash
     pip install --upgrade youtube-dl
     ```

   - 更新后重试命令：

     ```bash
     youtube-dl https://www.youtube.com/watch?v=st3mUEub99E
     ```

2. **切换至 yt-dlp（推荐替代方案）**：
   - youtube-dl 已停止活跃维护，而其分支项目 yt-dlp 能更好地适应 YouTube 近期变更。安装 yt-dlp：

     ```bash
     sudo pip install yt-dlp
     ```

     随后使用：

     ```bash
     yt-dlp https://www.youtube.com/watch?v=st3mUEub99E
     ```

   - yt-dlp 能更有效地处理身份验证和 IP 限制。[](https://stackoverflow.com/questions/79049216/yt-dlp-error-sign-in-required-when-downloading-youtube-video)

3. **关闭 VPN 或更换服务器**：
   - 若使用 VPN，YouTube 可能将您的 IP 标记为可疑。尝试关闭 VPN 或切换至其他服务器：

     ```bash
     yt-dlp https://www.youtube.com/watch?v=st3mUEub99E
     ```

   - 据用户反馈，断开 VPN 或更换服务器后问题得到解决。[](https://www.reddit.com/r/youtubedl/comments/1e6bzu4/ytdlp_error_sign_in_to_confirm_youre_not_a_bot/)[](https://www.reddit.com/r/youtubedl/comments/1i48cey/you_tube_ytdlp_sign_in_to_confirm_youre_not_a_bot/?tl=en)

4. **使用 Cookie 进行身份验证**：
   - YouTube 可能要求登录验证以通过机器人检测。从已登录 YouTube 的浏览器导出 Cookie：
     - 安装浏览器扩展（如 Firefox 或 Chrome 的 "Export Cookies"）。
     - 登录 YouTube 后将 Cookie 导出为 `cookies.txt` 文件，随后通过以下命令调用：

       ```bash
       youtube-dl --cookies ~/path/to/cookies.txt https://www.youtube.com/watch?v=st3mUEub99E
       ```

       或使用 yt-dlp：

       ```bash
       yt-dlp --cookies ~/path/to/cookies.txt https://www.youtube.com/watch?v=st3mUEub99E
       ```

     - 亦可使用 `--cookies-from-browser firefox`（或将 `firefox` 替换为 `chrome`、`edge` 等）自动提取 Cookie：

       ```bash
       yt-dlp --cookies-from-browser firefox https://www.youtube.com/watch?v=st3mUEub99E
       ```

     - 注意：为避免账户被标记风险，请勿使用主要 Google 账户，建议使用临时账户。[](https://stackoverflow.com/questions/79049216/yt-dlp-error-sign-in-required-when-downloading-youtube-video)[](https://www.reddit.com/r/youtubedl/comments/1e6bzu4/ytdlp_error_sign_in_to_confirm_youre_not_a_bot/)[](https://www.reddit.com/r/youtubedl/comments/1i48cey/you_tube_ytdlp_sign_in_to_confirm_youre_not_a_bot/?tl=en)

5. **使用代理**：
   - 若问题持续，可能是 IP 被屏蔽（例如使用数据中心 IP）。尝试通过住宅代理隐藏真实 IP：

     ```bash
     youtube-dl --proxy "http://proxy_address:port" https://www.youtube.com/watch?v=st3mUEub99E
     ```

     或使用 yt-dlp：

     ```bash
     yt-dlp --proxy "http://proxy_address:port" https://www.youtube.com/watch?v=st3mUEub99E
     ```

   - 住宅代理被标记的概率远低于数据中心代理。[](https://apify.com/epctex/youtube-video-downloader/issues/sign-in-to-confirm-y-1hjZd7SOtg8iLxyvN)

6. **清除缓存或更换网络**：
   - 若近期清理过日志或临时文件，请确保 youtube-dl/yt-dlp 未依赖损坏的缓存。清除缓存：

     ```bash
     rm -rf ~/.cache/youtube-dl
     rm -rf ~/.cache/yt-dlp
     ```

   - 切换至其他网络（如手机热点）测试是否与 IP 相关。[](https://forum.dvdfab.cn/forum/streamfab-support/streamfab/455389-sign-in-to-confirm-you-re-not-a-bot-help-please-with-yt-downloader)

7. **调试模式输出详细信息**：
   - 若上述步骤均无效，可通过调试模式运行命令以获取诊断信息：

     ```bash
     youtube-dl -v https://www.youtube.com/watch?v=st3mUEub99E
     ```

     或使用 yt-dlp：

     ```bash
     yt-dlp -v https://www.youtube.com/watch?v=st3mUEub99E
     ```

   - 可将输出内容分享至相关论坛（如 yt-dlp 的 GitHub issues）寻求社区帮助。[](https://github.com/yt-dlp/yt-dlp/issues/10128)

**注意事项**：

- YouTube 的机器人检测机制日趋严格，常针对数据中心 IP 或未验证请求。[](https://github.com/jagrosh/MusicBot/issues/1588)
- 使用 Cookie 存在账户被标记的较低风险，建议使用次要账户。[](https://stackoverflow.com/questions/79049216/yt-dlp-error-sign-in-required-when-downloading-youtube-video)
- 若视频为私享或受限内容，请确保账户具备访问权限再使用 Cookie。[](https://askubuntu.com/questions/776122/how-to-resolve-sign-in-error-when-using-youtube-dl-for-downloading-my-personal)
- 若所有方案均无效，可考虑使用替代前端如 Invidious 或 NewPipe，但可能存在功能限制。[](https://www.reddit.com/r/youtubedl/comments/1ihxrjm/getting_error_sign_in_to_confirm_youre_not_a_bot/)

请按顺序尝试上述步骤，建议优先更新或切换至 yt-dlp，这通常是最有效的解决方案。若问题仍然存在，请提供调试输出或具体细节（如 VPN 使用情况、操作系统等）。

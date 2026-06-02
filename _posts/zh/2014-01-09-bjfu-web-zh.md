---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 北京林业大学登录系统分析
translated: true
type: post
---

这篇文章最初在中文中撰写并发布在[CSDN](https://blog.csdn.net/lzw_java/article/details/18049581)上。

---

本文详细介绍了对北京林业大学网络登录系统的逆向工程过程。目标是通过程序模拟登录过程，有效地仿真用户通过网页浏览器连接到网络的操作。

通过使用Chrome的开发者工具，可以观察到登录过程中的网络请求。

第一个请求是发送到 `CheckLogin.jsp`，随后由 `CheckLogin.jsp` 触发对 `index.jsp` 的请求。

让我们更仔细地看看 `CheckLogin.jsp`。

可以看到，它使用了一个POST请求并且包含了几个键值对。但 `action` 是什么呢？

通过检查开发者工具中的“表单数据”，可以查看源代码：

要找到 `action` 的实际值，可以检查页面源代码：

`action` 值是第二行中的字符串。

现在，如何获取IP地址？登录系统可以在校园的任何地方访问，无论是通过Wi-Fi还是寝室的有线连接。IP地址是动态的。如何自动获取它？

还记得第一张图片吗？

网页会自动提供IP地址。登录系统知道哪个IP在访问它。我们可以从网页中提取它。

Chrome提供了方便的工具，可以快速定位网页代码的特定部分。Firefox有类似的插件，称为Firebug。

使用“检查元素”工具（放大镜图标），可以点击页面上的IP地址。

开发者工具将显示HTML结构，揭示IP地址在带有类 `login_txt` 的 `<span>` 标签中，具体位于其文本内容中。

Jsoup的 `select` 函数可以查找匹配CSS查询的元素，而 `first()` 返回第一个匹配的元素。

有了所有的键值对，我们现在可以模拟登录过程。

POST请求在请求体中发送键值对。`post.abort()` 调用中断了请求。这是因为我们将重用 `httpClient` 进行后续请求。`org.apache.http` 类尽量重用HTTP连接。如果请求没有终止，使用相同连接发送另一个请求可能会导致异常。

为什么我们需要重用 `httpClient`？我稍后会解释。

提交到 `checkLogin.jsp` 并不足以连接到网络。这个JSP只检查用户名和密码是否正确。

通过添加一个打印语句，可以看到响应代码。

200响应表示成功登录，303表示凭据不正确，404表示连接错误。

执行的第二个JSP脚本是 `index.jsp`，这是一个GET请求。

在这之后，我们仍然无法连接到网络。我们需要模拟请求到 `connect_action.jsp`，它需要一个 `userid` 参数（例如，`userid=88888`），对应于学生的ID。我注意到，前一个学生的 `userid` 仅比我的小1。如何获取这个值？

幸运的是，我记得我们从网页中提取了IP地址。我们可以做同样的事情来获取 `userid`？

这张截图是从断开连接页面获取的，但相同的逻辑适用于 `connect.jsp`。第二个JSP返回的页面的源代码包含了下一个我们需要请求的JSP的键值对。

在这里，我们使用正则表达式。`group(0)` 是整个匹配（例如，`userid=88888`），`group(1)` 是括号内的内容（例如，`88888`）。`\d` 匹配任何数字，`+` 表示一个或多个。`find()` 检查表达式是否匹配字符串的任何部分，而 `matches()` 检查表达式是否匹配整个字符串。因此，如果 `src` 类似于 `<frame userid=88888&ip="`，`matches()` 将返回 `false`，因为正则表达式不匹配整个字符串。

这是Java代码：

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.utils.URLEncodedUtils;
import org.apache.http.cookie.Cookie;
import org.apache.http.impl.client.AbstractHttpClient;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Login{

 static void print(String format, Object... args) {
  System.out.println(String.format(format, args));
 }

 public static void main(String[] args) {
  HttpClient httpClient = new DefaultHttpClient();
  String ip;
  String userId;
  String username="130888888";
  String password = "88888888";

  ip=cssQueryFirstText("http://login.bjfu.edu.cn/index.jsp","span.login_txt");

  doPost(httpClient,"http://login.bjfu.edu.cn/checkLogin.jsp",
    "username",username,"password",password,
    "ip",ip,"action","checkLogin.jsp");
  String content=doGet(httpClient,"http://login.bjfu.edu.cn/user/index.jsp",
    "ip",ip,"action","connect");
  userId=userId(content);
  doGet(httpClient,"http://login.bjfu.edu.cn/user/network/connect_action.jsp",
   "userid",userId,"ip",ip,"type","2");
 }

 static String userId(String html){
  Document doc=Jsoup.parse(html);
  Element elem=doc.select("frame#main").first();
  String src=elem.attr("src");
  Pattern pattern=Pattern.compile("userid=(\\d+)");
  Matcher matcher=pattern.matcher(src);
  String ans="";
  if(matcher.find()){
    ans=matcher.group(1);
  }
  return ans;
 }

 static String cssQueryFirstText(String url,String cssQuery) {
  String ip=null;
  try{
   Document doc=Jsoup.connect(url).get();
   Elements elems=doc.select(cssQuery);
   Element elem=elems.first();
   ip=elem.text();
  }catch(Exception e){
   e.printStackTrace();
  }
  return ip;
 }

 static String doGet(HttpClient httpClient, String url, String... pairs) {
  String entityContent=null;
  try {
   url = makeGetSrl(url, pairs);
   HttpGet get = new HttpGet(url);
   HttpResponse response = httpClient.execute(get);
   //print("%d", response.getStatusLine().getStatusCode());
   entityContent = entity(response);
   EntityUtils.consume(response.getEntity());
  } catch (IOException e) {
   e.printStackTrace();
  }
  return entityContent;
 }

 static void printEntity(HttpResponse rp){
  print("%s",entity(rp));
 }

 static String entity(HttpResponse response) {
  StringBuilder sb = new StringBuilder("");
  try {
   HttpEntity entity = response.getEntity();
   if (entity != null) {
    BufferedReader br = new BufferedReader(new InputStreamReader(
      entity.getContent()));
    String line = null;
    while ((line = br.readLine()) != null) {
     sb.append(line + "\n");
    }
   }
  } catch (Exception e) {
   e.printStackTrace();
  }
  return sb.toString();
 }

 static String makeGetSrl(String url,String... pairs) {
  if(!url.endsWith("?")){
   url+="?";
  }
  List<NameValuePair>params=new LinkedList<NameValuePair>();
  int len=pairs.length;
  for(int i=0;i<len/2;i++){
   params.add(new BasicNameValuePair(pairs[2*i],pairs[2*i+1]));
  }
  String paramsStr=URLEncodedUtils.format(params,"utf-8");
  url+=paramsStr;
  return url;
 }

 static String doPost(HttpClient httpClient, String url, String... pairs) {
  String entityContent = null;
  try {
   HttpPost post = new HttpPost(url);
   List<NameValuePair> params = new ArrayList<NameValuePair>();
   for (int i = 0; i < pairs.length / 2; i++) {
    params.add(new BasicNameValuePair(pairs[2 * i], pairs[2 * i + 1]));
   }
   post.setEntity(new UrlEncodedFormEntity(params, HTTP.UTF_8));
   HttpResponse response = httpClient.execute(post);
   entityContent = entity(response);
   //print("%d", response.getStatusLine().getStatusCode());
   post.abort();
  } catch (Exception e) {
   e.printStackTrace();
  }
  return entityContent;
 }

 private static String getCookies(HttpClient client) {
        StringBuilder sb = new StringBuilder();
        List<Cookie> cookies = ((AbstractHttpClient)
          client).getCookieStore().getCookies();
        for(Cookie cookie: cookies)
            sb.append(cookie.getName() + "=" + cookie.getValue() + ";");
        return sb.toString();
   }
}
```

完整的源代码可以在GitHub上找到。请注意，您可能需要一个有效的大学网络账户才能运行它。

重用相同的 `HttpClient` 的原因是它会自动存储cookie。JSP脚本使用cookie来确定请求是否来自同一个会话。这就是为什么从淘宝复制一个URL到另一个浏览器可能会导致超时错误。

`jsoup` 和正则表达式是非常有用的工具。有在线工具可以练习正则表达式。享受使用它们吧！

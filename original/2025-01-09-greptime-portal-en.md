---
audio: false
generated: false
image: false
lang: en
layout: post
title: Circular Graphic Overflow in GreptimeDB Portal
translated: false
type: post
---

I submitted a GitHub issue, <https://github.com/GreptimeTeam/docs/issues/1455>, titled "GreptimeDB Portal: Large Purple Circular Graphic Exceeds the Viewport Boundaries on Smaller Screens."

![gt_1](https://github.com/user-attachments/assets/d191f9c7-a8c6-4ba6-96c5-9388f69bef30)

This issue significantly impacts the user experience. It causes the entire homepage or screen to become easily draggable and difficult to control, especially affecting the bottom area. The problem becomes noticeable after scrolling for a while on the homepage.

ChatGPT:

The primary issue with the GreptimeDB portal's mobile responsiveness is that the large purple circular graphic exceeds the viewport boundaries on smaller screens. This problem arises due to the following factors:

1. **Fixed Positioning Without Responsive Adjustments**: The purple shape is likely positioned using fixed or absolute values that don't adapt to varying screen sizes. Without responsive design considerations, such elements can overflow the viewport on mobile devices.

2. **Lack of Media Queries**: Media queries are essential for applying different styles based on screen dimensions. The absence of media queries means that the same styles are applied across all devices, leading to layout issues on smaller screens.

3. **Viewport Meta Tag Missing**: The absence of a viewport meta tag can cause improper scaling on mobile devices. Including `<meta name="viewport" content="width=device-width, initial-scale=1.0">` in the `<head>` section ensures the page adapts to various screen sizes.

**Recommendations to Address the Issue:**

- **Implement Responsive Positioning**: Utilize relative units (e.g., percentages) and responsive design techniques to ensure the purple shape scales appropriately across different screen sizes.

- **Apply Media Queries**: Incorporate CSS media queries to adjust the size and position of the purple shape based on the device's screen dimensions. This approach allows for tailored styling that enhances the mobile viewing experience.

- **Add Viewport Meta Tag**: Ensure the inclusion of the viewport meta tag in the HTML `<head>` section to facilitate proper scaling and rendering on mobile devices.

By addressing these aspects, the GreptimeDB portal can achieve a more polished and user-friendly appearance on mobile browsers.

## Update

It has been fixed by the GreptimeDB team.

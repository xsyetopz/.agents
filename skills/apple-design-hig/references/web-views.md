---
title: "Web views"
source: https://developer.apple.com/design/human-interface-guidelines/web-views
retrieved: 2026-07-25
---
# Web views

A web view loads and displays rich web content, such as embedded HTML and websites, directly within your app.

*Image description: A stylized representation of a compass icon. The image is tinted red to subtly reflect the red in the original six-color Apple logo.*

For example, Mail uses a web view to show HTML content in messages.

## Best practices

**Support forward and back navigation when appropriate.** Web views support forward and back navigation, but this behavior isn’t available by default. If people are likely to use your web view to visit multiple pages, allow forward and back navigation, and provide corresponding controls to initiate these features.

**Avoid using a web view to build a web browser.** Using a web view to let people briefly access a website without leaving the context of your app is fine, but Safari is the primary way people browse the web. Attempting to replicate the functionality of Safari in your app is unnecessary and discouraged.

## Platform considerations

*No additional considerations for iOS, iPadOS, macOS, or visionOS. Not supported in tvOS or watchOS.*

## Resources

#### Related

[Webkit.org](https://webkit.org/)

#### Developer documentation

[WKWebView](https://developer.apple.com/documentation/WebKit/WKWebView) - WebKit

#### Videos

- [Explore WKWebView additions](https://developer.apple.com/videos/play/wwdc2021/10032)

## References

- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines)
- [Components](https://developer.apple.com/design/human-interface-guidelines/components)
- [Content](https://developer.apple.com/design/human-interface-guidelines/content)
- [Technologies](https://developer.apple.com/documentation/technologies)

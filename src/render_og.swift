// Renders assets/og.png (1200×630) for link previews, in the site's own language: paper background,
// the floor-plan grid, the house mark and the headline.
//
//   swift src/render_og.swift assets/og.png
import CoreGraphics
import CoreText
import Foundation
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32, _ a: CGFloat = 1) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 0xFF) / 255, green: CGFloat((hex >> 8) & 0xFF) / 255,
            blue: CGFloat(hex & 0xFF) / 255, alpha: a)
}

let W = 1200, H = 630
let out = URL(fileURLWithPath: CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "og.png")
let space = CGColorSpace(name: CGColorSpace.sRGB)!
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: space,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!

// Paper
ctx.setFillColor(rgb(0xF7F6F2)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))

// Green glow top-right
let glow = CGGradient(colorsSpace: space, colors: [rgb(0x1E6B5C, 0.28), rgb(0x1E6B5C, 0)] as CFArray, locations: [0, 1])!
ctx.drawRadialGradient(glow, startCenter: CGPoint(x: 1050, y: 520), startRadius: 0,
                       endCenter: CGPoint(x: 1050, y: 520), endRadius: 520, options: [])

// Floor-plan grid, fading to the left
ctx.saveGState()
let mask = CGGradient(colorsSpace: space, colors: [rgb(0x000000, 0), rgb(0x000000, 1)] as CFArray, locations: [0, 1])!
let gridLayer = CGLayer(ctx, size: CGSize(width: W, height: H), auxiliaryInfo: nil)!
let g = gridLayer.context!
g.setStrokeColor(rgb(0x141413, 0.09)); g.setLineWidth(1)
var v: CGFloat = 36
while v < CGFloat(W) { g.move(to: CGPoint(x: v, y: 0)); g.addLine(to: CGPoint(x: v, y: CGFloat(H))); v += 72 }
v = 27
while v < CGFloat(H) { g.move(to: CGPoint(x: 0, y: v)); g.addLine(to: CGPoint(x: CGFloat(W), y: v)); v += 72 }
g.strokePath()
// Fade: draw the layer through a horizontal alpha mask by clipping with a gradient-filled image
let maskCtx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                        space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGImageAlphaInfo.none.rawValue)!
let grayMask = CGGradient(colorsSpace: CGColorSpaceCreateDeviceGray(),
                          colors: [CGColor(gray: 0, alpha: 1), CGColor(gray: 1, alpha: 1)] as CFArray, locations: [0, 1])!
maskCtx.drawLinearGradient(grayMask, start: CGPoint(x: 300, y: 0), end: CGPoint(x: 1100, y: 0), options: [.drawsBeforeStartLocation, .drawsAfterEndLocation])
ctx.clip(to: CGRect(x: 0, y: 0, width: W, height: H), mask: maskCtx.makeImage()!)
ctx.draw(gridLayer, at: .zero)
ctx.restoreGState()
_ = mask

// Brand: rounded square + house, then wordmark
func roundedRect(_ r: CGRect, _ radius: CGFloat) -> CGPath { CGPath(roundedRect: r, cornerWidth: radius, cornerHeight: radius, transform: nil) }
let markRect = CGRect(x: 80, y: CGFloat(H) - 80 - 64, width: 64, height: 64)
ctx.addPath(roundedRect(markRect, 18)); ctx.setFillColor(rgb(0x1E6B5C)); ctx.fillPath()
// house path on 64 grid (y down in SVG → flip)
let pts: [(CGFloat, CGFloat)] = [(18, 46), (18, 28), (32, 17), (46, 28), (46, 46), (36, 46), (36, 34), (28, 34), (28, 46)]
let house = CGMutablePath()
for (i, p) in pts.enumerated() {
    let pt = CGPoint(x: markRect.minX + p.0, y: markRect.maxY - p.1)
    i == 0 ? house.move(to: pt) : house.addLine(to: pt)
}
house.closeSubpath()
ctx.addPath(house); ctx.setFillColor(rgb(0xFFFFFF)); ctx.fillPath()

func draw(_ text: String, font: CTFont, color: CGColor, at origin: CGPoint, tracking: CGFloat = 0) {
    let attrs: [NSAttributedString.Key: Any] = [
        NSAttributedString.Key(kCTFontAttributeName as String): font,
        NSAttributedString.Key(kCTForegroundColorAttributeName as String): color,
        NSAttributedString.Key(kCTKernAttributeName as String): tracking,
    ]
    let line = CTLineCreateWithAttributedString(NSAttributedString(string: text, attributes: attrs))
    ctx.textPosition = origin
    CTLineDraw(line, ctx)
}

let inter = CTFontCreateWithName("HelveticaNeue-Bold" as CFString, 34, nil)
draw("Nabo", font: inter, color: rgb(0x141413), at: CGPoint(x: 160, y: CGFloat(H) - 80 - 46), tracking: -0.5)

// Headline in a serif, two lines; the second italic green
let serif = CTFontCreateWithName("Georgia" as CFString, 86, nil)
let serifItalic = CTFontCreateWithName("Georgia-Italic" as CFString, 86, nil)
draw("Your building,", font: serif, color: rgb(0x141413), at: CGPoint(x: 76, y: 290), tracking: -2.5)
draw("together.", font: serifItalic, color: rgb(0x1E6B5C), at: CGPoint(x: 76, y: 190), tracking: -2.5)

// Footer line
let small = CTFontCreateWithName("HelveticaNeue-Medium" as CFString, 24, nil)
draw("A private community app for one apartment building", font: small, color: rgb(0x5C5B57), at: CGPoint(x: 80, y: 70))

// Language chips, bottom right
let chipFont = CTFontCreateWithName("HelveticaNeue-Bold" as CFString, 16, nil)
var x: CGFloat = CGFloat(W) - 80
for code in ["ES", "DE", "IT", "FR", "EN", "SQ"] {
    let w: CGFloat = 52
    x -= w
    let r = CGRect(x: x, y: 60, width: w - 8, height: 34)
    ctx.addPath(roundedRect(r, 17)); ctx.setFillColor(rgb(0xFFFFFF)); ctx.fillPath()
    ctx.addPath(roundedRect(r, 17)); ctx.setStrokeColor(rgb(0xDDDBD3)); ctx.setLineWidth(1); ctx.strokePath()
    draw(code, font: chipFont, color: rgb(0x5C5B57), at: CGPoint(x: r.minX + 10, y: r.minY + 10), tracking: 1)
}

let image = ctx.makeImage()!
let dest = CGImageDestinationCreateWithURL(out as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, image, nil)
CGImageDestinationFinalize(dest)
print("wrote \(out.path)")

// Render only the old proof pages carrying the tangent and explicitness boundary.
// Uses macOS PDFKit; does not install packages, launch a viewer, or modify input.
import AppKit
import PDFKit
import Foundation

let args = CommandLine.arguments
guard args.count == 3 else { fatalError("usage: swift render_lineage_pdf.swift INPUT.pdf OUTPUT_DIR") }
let input = URL(fileURLWithPath: args[1])
let output = URL(fileURLWithPath: args[2])
guard let pdf = PDFDocument(url: input) else { fatalError("cannot open PDF") }
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
for index in [7, 12] {
    guard let page = pdf.page(at: index) else { fatalError("missing PDF page") }
    let rect = page.bounds(for: .mediaBox)
    let width = Int(rect.width * 1.5), height = Int(rect.height * 1.5)
    guard let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
        colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0),
        let context = NSGraphicsContext(bitmapImageRep: rep) else { fatalError("bitmap failed") }
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = context
    context.cgContext.setFillColor(NSColor.white.cgColor)
    context.cgContext.fill(CGRect(x: 0, y: 0, width: width, height: height))
    context.cgContext.scaleBy(x: 1.5, y: 1.5)
    page.draw(with: .mediaBox, to: context.cgContext)
    NSGraphicsContext.restoreGraphicsState()
    guard let png = rep.representation(using: .png, properties: [:]) else { fatalError("PNG failed") }
    let target = output.appendingPathComponent("fable-proof-page-\(index+1).png")
    try png.write(to: target)
    print(target.path)
}

// Small built-in macOS PDFKit renderer; no package installation is needed.
// Usage: swift -module-cache-path /private/tmp/astra-pdf-swift-cache \
//   render_pdf_page.swift input.pdf zeroBasedPage output.png
import AppKit
import PDFKit
let args = CommandLine.arguments
guard args.count == 4,
      let doc = PDFDocument(url: URL(fileURLWithPath: args[1])),
      let index = Int(args[2]), let page = doc.page(at: index) else {
    fatalError("Expected readable PDF, zero-based page index, output PNG")
}
let image = page.thumbnail(of: NSSize(width: 1400, height: 2000), for: .mediaBox)
guard let tiff = image.tiffRepresentation,
      let bitmap = NSBitmapImageRep(data: tiff),
      let png = bitmap.representation(using: .png, properties: [:]) else {
    fatalError("PDFKit rasterization failed")
}
try png.write(to: URL(fileURLWithPath: args[3]))
print("Rendered page \(index) of \(doc.pageCount) to \(args[3])")

/* Lightweight macOS CoreGraphics renderer for exact old-proof pages 8 and 13.
 * No input mutation, package installation, or application launch.
 * Compile: clang -fno-modules -framework ApplicationServices -framework ImageIO
 *          -framework CoreServices render_lineage_pdf.c -o render_lineage_pdf
 * Run: render_lineage_pdf INPUT.pdf EXISTING_OUTPUT_DIRECTORY
 */
#include <ApplicationServices/ApplicationServices.h>
#include <ImageIO/ImageIO.h>
#include <CoreServices/CoreServices.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

int main(int argc, char **argv) {
    assert(argc==3);
    CFURLRef input=CFURLCreateFromFileSystemRepresentation(NULL,(UInt8*)argv[1],strlen(argv[1]),false);
    CGPDFDocumentRef pdf=CGPDFDocumentCreateWithURL(input);
    assert(pdf);
    int numbers[2]={8,13};
    for(int n=0;n<2;n++) {
        CGPDFPageRef page=CGPDFDocumentGetPage(pdf,numbers[n]); assert(page);
        CGRect box=CGPDFPageGetBoxRect(page,kCGPDFMediaBox);
        size_t w=(size_t)(box.size.width*1.5),h=(size_t)(box.size.height*1.5);
        CGColorSpaceRef colors=CGColorSpaceCreateDeviceRGB();
        CGContextRef ctx=CGBitmapContextCreate(NULL,w,h,8,0,colors,kCGImageAlphaPremultipliedLast);
        assert(ctx); CGContextSetRGBFillColor(ctx,1,1,1,1);
        CGContextFillRect(ctx,CGRectMake(0,0,w,h));
        CGContextScaleCTM(ctx,1.5,1.5); CGContextDrawPDFPage(ctx,page);
        CGImageRef image=CGBitmapContextCreateImage(ctx); assert(image);
        char name[4096]; snprintf(name,sizeof(name),"%s/fable-proof-page-%d.png",argv[2],numbers[n]);
        CFURLRef output=CFURLCreateFromFileSystemRepresentation(NULL,(UInt8*)name,strlen(name),false);
        CGImageDestinationRef dest=CGImageDestinationCreateWithURL(output,kUTTypePNG,1,NULL); assert(dest);
        CGImageDestinationAddImage(dest,image,NULL); assert(CGImageDestinationFinalize(dest));
        printf("%s\n",name);
        CFRelease(dest); CFRelease(output); CGImageRelease(image);
        CGContextRelease(ctx); CGColorSpaceRelease(colors);
    }
    CGPDFDocumentRelease(pdf); CFRelease(input); return 0;
}

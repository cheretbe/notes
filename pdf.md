### Combine to PDF
```shell
apt install imagemagick
```
Fix "convert-im6.q16: attempt to perform an operation not allowed by the security policy PDF' @ error/constitute.c/IsCoderAuthorized/408" error in `/etc/ImageMagick-6/policy.xml`:
```xml
<policymap>
  <!-- Replace "none" to "read:write" for PDF files -->
  <policy domain="coder" rights="read:write" pattern="PDF" />
</policymap>
```
```shell
# JPEG to PDF
convert file1.jpg file2.jpg result.pdf
# PNG to PDF with JPEG conversion (reduces size)
convert file1.png file2.png -compress jpeg -quality 80 result.pdf
```

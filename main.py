import webapp2
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
import urllib


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)


upload_form = """
<html>
    <body>
        <form action="%s" method="POST" enctype="multipart/form-data">
        Upload File: <input type="file" name="file"><br>
        <input type="submit" name="submit" value="submit">
        </form>
    </body>
</html>"""


class AddImagePage(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/serve/_ah/upload_image')
        self.response.out.write(upload_form % upload_url)


class AddFilePage(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/serve/_ah/upload_file')
        self.response.out.write(upload_form % upload_url)


class UploadFileHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]

        self.response.out.write(str('http://%s/serve/static/%s' % (self.request.host, blob_info.key())))


class UploadImageHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]

        serve_url = images.get_serving_url(blob_info.key())

        self.response.out.write(serve_url)


app = webapp2.WSGIApplication([
    (r'/serve/add_image', AddImagePage),
    (r'/serve/add_file', AddFilePage),
    (r'/serve/_ah/upload_image', UploadImageHandler),
    (r'/serve/_ah/upload_file', UploadFileHandler),

    (r'/serve/static/([^/]+)?', ServeHandler),
])

import webapp2, requests
import httplib, urllib2, json
import cloudstorage as gcs
import datetime


class ImageUpload(webapp2.RequestHandler):
    def post(self):

        urlList = []
        file = self.request.POST.getall('file')
        profileId = self.request.get('profileId')

        courseId = self.request.get('courseId')

        title = self.request.get('title')

        desc = self.request.get('desc')
        print len(file)
        print "_____________________________________________________-"
        type = self.request.get('type')
        bucketName = "/uploadnotes-2016.appspot.com"
        for file in self.request.POST.getall('file'):

            timestamp = str(datetime.datetime.now())
            fileName = bucketName + '/' + courseId + '/' + profileId + '/' + timestamp + '.jpg'
            gcsFile = gcs.open(fileName, mode='w', content_type='image/jpeg', options={'x-goog-acl': 'public-read'})
            gcsFile.write(file.value)
            url = 'https://storage.googleapis.com'+fileName
            urlList.append(url)
            gcsFile.close()

        if type == 'notes':
            date = self.request.get('date')
            classNumber = self.request.get('classNumber')
            url = "https://uploadnotes-2016.appspot.com/_ah/api/notesapi/v1/createNotes"
            data = {'profileId': profileId, 'courseId': courseId, 'title': title, 'notesDesc': desc, 
                    'urlList': urlList, 'classNumber': classNumber, 'date': date}
            header = {'Content-Type':  'application/json; charset=UTF-8'}
            req = urllib2.Request(url, json.dumps(data), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            key = response.get('key')
            redirectUrl = str('https://salty-forest-16158.herokuapp.com/notebook?id=')+str(key)
            self.redirect(redirectUrl)
        if type == 'assignment':
            dueDate = self.request.get('dueDate')
            dueTime = self.request.get('dueTime')
            url = "https://uploadnotes-2016.appspot.com/_ah/api/notesapi/v1/createAssignment"
            data = {'uploaderId': profileId, 'courseId': courseId, 'assignmentTitle': title, 'assignmentDesc': desc, 'urlList': urlList, 'dueDate': dueDate, 'dueTime':dueTime}
            header = {'Content-Type':  'application/json; charset=UTF-8'}
            req = urllib2.Request(url, json.dumps(data), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            key = response.get('key')
            redirectUrl = str('https://salty-forest-16158.herokuapp.com/assignment?id=')+str(key)
            self.redirect(redirectUrl)
        if type == 'exam':
            dueDate = self.request.get('dueDate')
            dueTime = self.request.get('dueTime')
            url = "https://uploadnotes-2016.appspot.com/_ah/api/notesapi/v1/createExam"
            data = {'uploaderId': profileId, 'courseId': courseId, 'examTitle': title, 'examDesc': desc, 'urlList': urlList, 'dueDate': dueDate, 'dueTime':dueTime}
            header = {'Content-Type':  'application/json; charset=UTF-8'}
            req = urllib2.Request(url, json.dumps(data), header)
            response = urllib2.urlopen(req)
            response = json.loads(response.read())
            key = response.get('key')
            redirectUrl = str('https://salty-forest-16158.herokuapp.com/exam?id=')+str(key)
            self.redirect(redirectUrl)
    
    def get(self):
        self.response.write("""<html>
<head>
<style type="text/css">.thumb-image{float:left;width:100px;position:relative;padding:5px;}</style>
</head>
<body>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<form enctype="multipart/form-data" method="POST">

<input type="file" id="fileUpload" name="file" multiple>
<input type="text" name="profileId">
<input type="text" name="courseId">
<input type="text" name="title">
<input type="text" name="desc">
<input type="text" name="date">
<input type="text" name="classNumber">
<input type="text" name="dueDate">
<input type="text" name="dueTime">
<input type="text" name="type">
        <input type="submit" value="Submit">
</form>
<div id="image-holder"></div>

</div>

<script>
$(document).ready(function() {
        $("#fileUpload").on('change', function() {
          //Get count of selected files
          var countFiles = $(this)[0].files.length;
          var imgPath = $(this)[0].value;
          var extn = imgPath.substring(imgPath.lastIndexOf('.') + 1).toLowerCase();
          var image_holder = $("#image-holder");
          image_holder.empty();
          if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {
            if (typeof(FileReader) != "undefined") {
              //loop for each file selected for uploaded.
              for (var i = 0; i < countFiles; i++) 
              {
                var reader = new FileReader();
                reader.onload = function(e) {
                  $("<img />", {
                    "src": e.target.result,
                    "class": "thumb-image"
                  }).appendTo(image_holder);
                }
                image_holder.show();
                reader.readAsDataURL($(this)[0].files[i]);
              }
            } else {
              alert("This browser does not support FileReader.");
            }
          } else {
            alert("Pls select only images");
          }
        });
      });
</script>
</body>
</html>""")

app = webapp2.WSGIApplication([('/img', ImageUpload)
                              ], debug=True)
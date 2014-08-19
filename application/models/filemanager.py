from google.appengine.api import files

def save_file(file, filepath):
	writable_file_name=files.gs.create(filepath, mime_type=file.content_type, acl="public-read")

	with files.open(writable_file_name, 'ab') as f:
		f.write(file.read())
	files.finalize(writable_file_name)
	#if there is a change in file, you have to use finalize

def read_file(filepath):
	with files.open(filepath, 'r') as f:
		data = f.read()

	return data
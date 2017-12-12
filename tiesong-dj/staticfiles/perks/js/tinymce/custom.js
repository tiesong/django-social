tinymce.init({
  selector: 'div.tinymce',
  theme: 'inlite',
  plugins: 'image table link paste contextmenu textpattern autolink',
  insert_toolbar: 'quickimage quicktable',
  selection_toolbar: 'bold italic | quicklink h2 h3 blockquote',
  inline: true,
  paste_data_images: true,
  content_css: [
    '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
    '//www.tinymce.com/css/codepen.min.css']
});
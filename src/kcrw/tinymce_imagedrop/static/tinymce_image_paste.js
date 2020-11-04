tinymce.PluginManager.add('paste_plone_image', function(editor, url) {
  editor.on('PastePostProcess', function (e) {
    let blob_promises = [];
    let blob_ids = [];
    const images = e.node.getElementsByTagName('img');
    const context_url = $('body').data('base-url') || $('base').attr('href');
    const htmlToElement = function(html) {
      var template = document.createElement('template');
      html = html.trim(); // Never return a text node of whitespace as the result
      template.innerHTML = html;
      return template.content.firstChild;
    }
    const blob_resolver = function (blob) {
      const file_reader = new FileReader();
      return new Promise((resolve, reject) => {
        file_reader.onerror = () => {
          file_reader.abort();
          reject(new DOMException("Problem parsing input file."));
        };

        file_reader.onload = () => {
          resolve(btoa(file_reader.result));
        };
        file_reader.readAsBinaryString(blob);
      });
    };
    const handle_failure = function(blob_id) {
      let img = editor.contentDocument.getElementById('blob-' + blob_id);
      let current_container = img.parentNode;
      let error = editor.contentDocument.createElement('span');
      error.classList.add('error');
      error.textContent = ' Error uploading image. See logs for details. ';
      current_container.insertBefore(error, img);
      img.remove();
    };
    const upload_blobs_for_imgs = function (files) {
      $.ajax({
        url: context_url + '/@@create-dropped-images',
        method: 'POST',
        data: {
          files: JSON.stringify(files),
          _authenticator: $('input[name="_authenticator"]').val()
        },
        dataType: 'json'
      }).done(function (result) {
        for (let i = 0; i < result.images.length; i++) {
          let new_elem = htmlToElement(result.images[i]);
          let img = editor.contentDocument.getElementById('blob-' + blob_ids[i]);
          if (img) {
            let current_container = img.parentNode;
            if (new_elem.tagName == 'DIV' || new_elem.tagName == 'P') {
              if (current_container.children.length == 1 && !current_container.textContent.trim()) {
                current_container.parentNode.replaceChild(new_elem, current_container);
                continue;
              } else if (current_container.tagName == 'P' || current_container.tagName[0] == 'H') {
                img.remove();
                current_container.after(new_elem);
                continue;
              }
            }
            current_container.replaceChild(new_elem, img);
          }
        }
      }).fail(function () {
        for (let i = 0; i < blob_ids.length; i++) {
          handle_failure(blob_ids[i]);
        }
      });
    };
    const failure_handler = function (img, blob_id) {
      return function () {
        img.remove();
        handle_failure(blob_id);
      };
    };
    for (let i = 0; i < images.length; i++) {
      let promise;
      let img = images[i];
      let blob_url = img.src;
      let blob_id = blob_url.split('/').pop();
      blob_ids.push(blob_id);
      img.id = 'blob-' + blob_id;
      if (blob_url.indexOf('blob:') == 0) {
        promise = fetch(blob_url).then(res => res.blob()).then(blob_resolver).catch(
          failure_handler(img, blob_id)
        );
      }
      blob_promises.push(promise);
    }
    Promise.all(blob_promises).then(upload_blobs_for_imgs);
  });
  return {
    getMetadata: function () {
      return  {
        name: "Image Drop/Paste Plugin",
        url: "http://github.com/KCRW-org"
      };
    }
  };
});

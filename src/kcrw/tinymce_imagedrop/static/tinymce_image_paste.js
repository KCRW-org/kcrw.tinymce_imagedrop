tinymce.PluginManager.add('paste_plone_image', function(editor, url) {
  const create_set = function (array) {
    let new_set = new Set();
    for (i = 0; i < array.length; i++) {
      new_set.add(array[i]);
    }
    return new_set;
  };
  const ALLOWED_BLOCK_CONTAINERS = [
    'HTML', 'BODY', 'HEADER', 'FOOTER', 'DIV', 'MAIN',
    'SECTION', 'ARTICLE', 'ASIDE', 'FIELDSET', 'FORM',
    'BLOCKQUOTE'
  ];
  const CONTAINER_CHECKER = create_set(ALLOWED_BLOCK_CONTAINERS);
  const BLOCK_CHECKER = create_set(
    ALLOWED_BLOCK_CONTAINERS.concat([
      'P', 'UL', 'OL', 'DL', 'FIGURE', 'TABLE'
    ])
  );
  const insertion_point = function (container) {
    let wrapper = container;
    let sibliing = container;
    while (wrapper && !CONTAINER_CHECKER.has(wrapper.tagName)) {
      sibling = wrapper;
      wrapper = wrapper.parentNode;
    }
    return sibling
  };

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
    const start_replace = function() {
      const el_name = editor.getElement().name;
      let controls = Array.from(document.getElementsByClassName('submit-widget')).concat(
        Array.from(document.getElementsByName('form.button.save'))).concat(
        Array.from(document.getElementsByName('form.button.cancel'))).concat(
        Array.from(document.getElementsByName(el_name + '.mimeType'))).concat(
        Array.from(document.getElementsByName(el_name + '_text_format')));
      for (let i = 0; i < controls.length; i++) {
        controls[i].disabled = true;
      }
    };
    const finish_replace = function() {
      const el_name = editor.getElement().name;
      let controls = Array.from(document.getElementsByClassName('submit-widget')).concat(
        Array.from(document.getElementsByName('form.button.save'))).concat(
        Array.from(document.getElementsByName('form.button.cancel'))).concat(
        Array.from(document.getElementsByName(el_name + '.mimeType'))).concat(
        Array.from(el_name + '_text_format'));
      for (let i = 0; i < controls.length; i++) {
        controls[i].disabled = false;
      }
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
        var place_before = false;
        for (let i = 0; i < result.images.length; i++) {
          let new_elem = htmlToElement(result.images[i]);
          let img = editor.contentDocument.getElementById('blob-' + blob_ids[i]);
          if (img) {
            let current_container = img.parentNode;
            if (BLOCK_CHECKER.has(new_elem.tagName)) {
              // If the image is the only thing in the container, replace the container with the new one.
              if (current_container.children.length == 1 && !current_container.textContent.trim()) {
                current_container.parentNode.replaceChild(new_elem, current_container);
                continue;
              } else {
                let wrapper = insertion_point(current_container);
                if (img.nextSibling && img.nextSibling.textContent) {
                  place_before = true;
                }
                img.remove();
                if (place_before) {
                  wrapper.before(new_elem);
                } else {
                  wrapper.after(new_elem);
                }
                continue;
              }
            }
            current_container.replaceChild(new_elem, img);
          }
        }
        finish_replace();
      }).fail(function () {
        for (let i = 0; i < blob_ids.length; i++) {
          handle_failure(blob_ids[i]);
        }
        finish_replace();
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
    start_replace();
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

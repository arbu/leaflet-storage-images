L.FormBuilder.FileInput = L.FormBuilder.Input.extend({
    build: function() {
        L.FormBuilder.Input.prototype.build.call(this);
        L.DomEvent.on(this.input, 'change', this.onChange, this);
    },
    type: function() {
        return 'file';
    },
    value: function() {
        return this.input.files[0];
    },
    fetch: function() {
        try {
            L.FormBuilder.Input.prototype.fetch.call(this);
        } catch(e) {
        }
    },
    onChange: function(e) {
        this.sync();
        if(this.options.onChange)
            this.options.onChange.call(this.options.onChangeContext, e);
    },
});


L.Storage.Marker.include({
    appendOrigEditFieldsets: L.Storage.Marker.prototype.appendEditFieldsets,
    appendEditFieldsets: function(container) {
        this.appendOrigEditFieldsets.call(this, container);
        var field = ['_image', {handler: 'FileInput', onChange: this.uploadImage, onChangeContext: this}];
        var builder = new L.S.FormBuilder(this, [field]);
        var fieldset = L.DomUtil.createFieldset(container, L._("Add image"));
        fieldset.appendChild(builder.build());
    },
    uploadImage: function(e) {
        var self = this, input = e.target, req = new XMLHttpRequest();
        input.disabled = true;
       
        req.upload.onprogress = function(e) {
            // TODO
        };
        req.onerror = function(e) {
            L.Storage.fire('ui:alert', {content: L._("Network error."), level: 'error'});
            delete self._image;
            this.edit();
        };
        req.onload = function(e) {
            console.log(e);
            console.log(req);
            if(req.status === 200) {
                self.addImage(req.response);
            } else {
                var msg = "";
                if(req.status === 413) {
                    msg = L._("The file is too large. Please try resizing it or use an external hoster.");
                } else if(req.status === 415 && req.response.image) {
                    for(var i = 0; i < req.response.image.length; i++) {
                        msg += L._(req.response.image[i].message) + " ";
                    }
                } else if(req.status) {
                    msg = "Error " + req.status + ": " + req.statusText;
                } else {
                    msg = L._("Upload aborted.");
                }
                L.Storage.fire('ui:alert', {content: msg, level: 'error', duration: 6000});
            }
            delete self._image;
            self.edit();
        };
        req.responseType = 'json';

        var data = new FormData();
        data.append('image', this._image);

        req.open("POST", "/image/add", true);
        req.send(data);
    },
    addImage: function(response) {
        var tag = "[[" + response.path + "|{{" + response.thumbnail + "}}]]";
        if(this.properties.description) {
            this.properties.description += "\n" + tag;
        } else {
            this.properties.description = tag;
        }
        if(response.location && confirm(L._("The image contains embedded GPS-coordinates. Do you want to move the marker to this location?"))) {
            var newLatLng = new L.LatLng(response.location.lat, response.location.lng);
            this.setLatLng(newLatLng);
        }
    },
});

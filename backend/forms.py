from flask_wtf import FlaskForm


class VueFrom(FlaskForm):

    def vue_field(self, field):
        field = getattr(self, field)
        data = {
            "name": field.name,
            "error": len(field.errors) > 0,
            "errors": field.errors if len(field.errors) > 0 else {}
        }
        if field.type == "SelectField":
            data.update({"choices": field.choices})
        if field.render_kw is not None:
            data.update({
                "placeholder": field.render_kw["placeholder"] if "placeholder" in field.render_kw else "",
                "disabled": field.render_kw["disabled"] if "disabled" in field.render_kw else False,
            })
        return data

    def vue_form(self):
        return {field: self.field_json(field) for field in self.data}

    def vue_errors(self):
        return [e for e in self.errors.values()]

    def vue_error_form(self):
        return {k: v for k, v in self.errors.items()}

    def vue_validated(self):
        return len(self.vue_errors()) == 0

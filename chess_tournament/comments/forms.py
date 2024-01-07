from django import forms


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), required=True)
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

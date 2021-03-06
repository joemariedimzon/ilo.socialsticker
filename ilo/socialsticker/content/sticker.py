from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
#from plone.multilingualbehavior.directives import languageindependent
from collective import dexteritytextindexer

from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer import idnormalizer

from ilo.socialsticker import MessageFactory as _


# Interface class; used to define content-type schema.

class ISticker(form.Schema, IImageScaleTraversable):
    """
    Sticker
    """

    title = schema.TextLine(
           title=_(u"Title"),
           required=True,
        )

    sticker_image = NamedBlobFile(
        title=u'Image',
        required=True,
    )

    default_message = schema.TextLine(
           title=_(u"Default Message"),
           required=True,
        )

    pass

alsoProvides(ISticker, IFormFieldProvider)

@grok.subscribe(ISticker, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides = ISticker.__identifier__)
    for brain in brains:
        object_Ids.append(brain.id)
    
    title = str(idnormalizer.normalize(context.title))
    temp_new_id = title
    new_id = temp_new_id.replace("-","")
    test = ''
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        if '-' not in (max(test)):
            new_id = new_id + '-1'
        if '-' in (max(test)):
            new_id = new_id +'-' +str(int(max(test).split('-')[-1])+1) 

    parent.manage_renameObject(id, new_id )
    new_title = title
    context.setTitle(context.title)

    context.reindexObject()
    return

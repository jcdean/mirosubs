// Universal Subtitles, universalsubtitles.org
// 
// Copyright (C) 2010 Participatory Culture Foundation
// 
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
// 
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see 
// http://www.gnu.org/licenses/agpl-3.0.html.

goog.provide('mirosubs.translate.TranslationPanel');

mirosubs.translate.TranslationPanel = function(subtitles, allLanguages, 
                                               unitOfWork, serverModel) {
    goog.ui.Component.call(this);
    this.subtitles_ = subtitles;
    this.languages_ = allLanguages;
    this.unitOfWork_ = unitOfWork;
    this.serverModel_ = serverModel;
    this.contentElem_ = null;
};
goog.inherits(mirosubs.translate.TranslationPanel, goog.ui.Component);
mirosubs.translate.TranslationPanel.prototype.getContentElement = function() {
    return this.contentElem_;
};
mirosubs.translate.TranslationPanel.prototype.createLanguageSelect_ = 
    function($d)
{
    var selectOptions = [ $d('option', {'value':'NONE'}, 
                             'Select Language...') ];
    goog.array.forEach(
        this.languages_, function(lang) {
            selectOptions.push(
                $d('option', {'value':lang['code']}, lang['name']));
        });
    return $d('select', null, selectOptions);
};
mirosubs.translate.TranslationPanel.prototype.createDom = function() {
    mirosubs.translate.TranslationPanel.superClass_.createDom.call(this);
    var el = this.getElement();
    var $d = goog.bind(this.getDomHelper().createDom, this.getDomHelper());
    this.languageSelect_ = this.createLanguageSelect_($d)
    el.appendChild($d('div', 'mirosubs-langDrop', 
                      goog.dom.createTextNode('To begin translating: '),
                      this.languageSelect_));
    this.getHandler().listen(
        this.languageSelect_, goog.events.EventType.CHANGE,
        this.languageSelected_);
    el.appendChild(this.contentElem_ = $d('div'));
    this.translationList_ = 
        new mirosubs.translate.TranslationList(
            this.subtitles_, this.unitOfWork_);
    this.addChild(this.translationList_, true);
    this.translationList_.getElement().className = 
        "mirosubs-titlesList taller";
    this.translationList_.setEnabled(false);
};
mirosubs.translate.TranslationPanel.prototype.languageSelected_ = 
    function(event) 
{
    var languageCode = this.languageSelect_.value;
    var that = this;
    // TODO: show loading animation
    this.translationList_.setEnabled(false);
    this.serverModel_.startTranslating(languageCode, 
        function(success, result) {
            if (!success)
                alert(result);
            else
                that.startEditing_(result);
        });
};
mirosubs.translate.TranslationPanel.prototype.startEditing_ = 
    function(existingTranslations) 
{
    var uw = this.unitOfWork_;
    var editableTranslations = 
        goog.array.map(
            existingTranslations, 
            function(transJson) {
                return new mirosubs.translate.EditableTranslation(
                    uw, transJson['caption_id'], transJson);
            });
    this.translationList_.setTranslations(editableTranslations);
    this.translationList_.setEnabled(true);
};

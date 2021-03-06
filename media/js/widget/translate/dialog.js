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

goog.provide('mirosubs.translate.Dialog');

mirosubs.translate.Dialog = function(videoSource, 
                                     videoID,
                                     subtitles, 
                                     allLanguages,
                                     nullWidget) {
    mirosubs.Dialog.call(this, videoSource);
    this.videoID_ = videoID;
    this.subtitles_ = subtitles;
    this.languages_ = allLanguages;
    this.unitOfWork_ = new mirosubs.UnitOfWork();
    this.serverModel_ = new mirosubs.translate.ServerModel(
        videoID, this.unitOfWork_, nullWidget,
        goog.bind(this.showLoginNag_, this));
    /**
     * Null unless "Done" gets clicked and translations get saved.
     * @type {?Array.<{'code':string, 'name':string}>}
     */
    this.availableLanguages_ = null;
};
goog.inherits(mirosubs.translate.Dialog, mirosubs.Dialog);
mirosubs.translate.Dialog.prototype.createDom = function() {
    mirosubs.translate.Dialog.superClass_.createDom.call(this);
    var translationPanel = new mirosubs.translate.TranslationPanel(
        this.subtitles_, this.languages_,
        this.unitOfWork_, this.serverModel_)
    this.getCaptioningAreaInternal().addChild(translationPanel, true);
    var rightPanel = this.createRightPanel_();
    this.setRightPanelInternal(rightPanel);
    this.getHandler().listen(
        rightPanel, mirosubs.RightPanel.EventType.DONE,
        this.handleDoneKeyPress_);
};
mirosubs.translate.Dialog.prototype.createRightPanel_ = function() {
    var helpContents = new mirosubs.RightPanel.HelpContents(
        "Adding a New Translation",
        [["Thanks for volunteering to translate! As soon as you submit ",
          "your translation, it will be available to everyone watching the ",
          "video in the widget."].join(''),
         ["Choose a language from the menu. Then translate each  ", 
          "line, one by one, in the white space below each line."].join('')]);
    var KC = goog.events.KeyCodes;
    var keySpecs = [
        new mirosubs.RightPanel.KeySpec(
            'mirosubs-play', 'mirosubs-tab', 'tab', 'Next Line', KC.TAB),
        new mirosubs.RightPanel.KeySpec(
            'mirosubs-play', 'mirosubs-tab', 'shift+tab', 'Previous Line',
            'shift+tab')
    ];
    return new mirosubs.RightPanel(
        this.serverModel_, helpContents, keySpecs, false, "Done?", 
        "Submit final translation");
};
mirosubs.translate.Dialog.prototype.handleDoneKeyPress_ = function(event) {
    var that = this;
    this.serverModel_.finish(function(availableLanguages) {
        that.availableLanguages_ = availableLanguages;
        that.setVisible(false);
    });
    event.preventDefault();
};
mirosubs.translate.Dialog.prototype.getAvailableLanguages = function() {
    return this.availableLanguages_;
};
mirosubs.translate.Dialog.prototype.showLoginNag_ = function() {
    // maybe implement this later, but we're leaving it out for now.
};
mirosubs.translate.Dialog.prototype.disposeInternal = function() {
    mirosubs.translate.Dialog.superClass_.disposeInternal.call(this);
    this.unitOfWork_.dispose();
    this.serverModel_.dispose();
};

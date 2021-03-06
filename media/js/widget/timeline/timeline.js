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

goog.provide('mirosubs.timeline.Timeline');

/**
 *
 * @param {number} spacing The space, in seconds, between two 
 *     major ticks.
 */
mirosubs.timeline.Timeline = function(spacing) {
    goog.ui.Component.call(this);
    this.spacing_ = spacing;
};
goog.inherits(mirosubs.timeline.Timeline, goog.ui.Component);
mirosubs.timeline.Timeline.prototype.createDom = function() {
    mirosubs.timeline.Timeline.superClass_.createDom.call(this);
    this.timeRow_ = new mirosubs.timeline.TimeRow(this.spacing_);
    this.addChild(this.timeRow_);
};
mirosubs.timeline.Timeline.prototype.setTime(time) {
    this.timeRow_.setTime(time);
    
};
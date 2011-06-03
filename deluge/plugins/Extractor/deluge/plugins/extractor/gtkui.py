#
# gtkui.py
#
# Copyright (C) 2009 Andrew Resch <andrewresch@gmail.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#
#

import gtk
import logging

from deluge.ui.client import client
from deluge.plugins.pluginbase import GtkPluginBase
import deluge.component as component
import deluge.common

from common import get_resource

log = logging.getLogger(__name__)

class GtkUI(GtkPluginBase):
    def enable(self):
        self.glade = gtk.glade.XML(get_resource("extractor_prefs.glade"))

        component.get("Preferences").add_page("Extractor", self.glade.get_widget("extractor_prefs_box"))
        component.get("PluginManager").register_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").register_hook("on_show_prefs", self.on_show_prefs)
        self.on_show_prefs()

    def disable(self):
        component.get("Preferences").remove_page("Extractor")
        component.get("PluginManager").deregister_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").deregister_hook("on_show_prefs", self.on_show_prefs)
        del self.glade

    def on_apply_prefs(self):
        log.debug("applying prefs for Extractor")
        if client.is_localhost():
            path = self.glade.get_widget("folderchooser_path").get_current_folder()
        else:
            path = self.glade.get_widget("entry_path").get_text()

        config = {
            "extract_path": path,
            "use_name_folder": self.glade.get_widget("chk_use_name").get_active()
        }

        client.extractor.set_config(config)

    def on_show_prefs(self):
        if client.is_localhost():
            self.glade.get_widget("folderchooser_path").show()
            self.glade.get_widget("entry_path").hide()
        else:
            self.glade.get_widget("folderchooser_path").hide()
            self.glade.get_widget("entry_path").show()

        def on_get_config(config):
            if client.is_localhost():
                self.glade.get_widget("folderchooser_path").set_current_folder(config["extract_path"])
            else:
                self.glade.get_widget("entry_path").set_text(config["extract_path"])

            self.glade.get_widget("chk_use_name").set_active(config["use_name_folder"])

        client.extractor.get_config().addCallback(on_get_config)

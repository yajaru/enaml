#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from PyQt4.QtCore import Qt, QPointF, QPoint

from atom.api import Typed

from enaml.widgets.popup_view import ProxyPopupView

from .q_popup_view import QPopupView
from .qt_widget import QtWidget


EDGES = {
    'left': QPopupView.LeftEdge,
    'right': QPopupView.RightEdge,
    'top': QPopupView.TopEdge,
    'bottom': QPopupView.BottomEdge,
}


WINDOW_TYPES = {
    'popup': Qt.Popup,
    'tool_tip': Qt.ToolTip,
}


class QtPopupView(QtWidget, ProxyPopupView):
    """ A Qt implementation of an Enaml ProxyPopupView.

    """
    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(QPopupView)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the QPopupView widget.

        """
        flags = WINDOW_TYPES[self.declaration.window_type]
        self.widget = QPopupView(self.parent_widget(), flags)

    def init_widget(self):
        """ Initialize the widget.

        """
        super(QtPopupView, self).init_widget()
        d = self.declaration
        self.set_anchor(d.anchor)
        self.set_parent_anchor(d.parent_anchor)
        self.set_arrow_size(d.arrow_size)
        self.set_arrow_edge(d.arrow_edge)
        self.set_arrow_position(d.arrow_position)
        self.set_offset(d.offset)
        self.set_timeout(d.timeout)
        self.set_fade_in_duration(d.fade_in_duration)
        self.set_fade_out_duration(d.fade_out_duration)
        self.widget.closed.connect(self.on_closed)

    def init_layout(self):
        """ Initialize the widget layout.

        """
        super(QtPopupView, self).init_layout()
        self.widget.setCentralWidget(self.central_widget())

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------
    def central_widget(self):
        """ Find and return the central widget child for this widget.

        Returns
        -------
        result : QWidget or None
            The central widget defined for this widget, or None if one
            is not defined.

        """
        d = self.declaration.central_widget()
        if d is not None:
            return d.proxy.widget

    #--------------------------------------------------------------------------
    # Signal Handlers
    #--------------------------------------------------------------------------
    def on_closed(self):
        """ The signal handler for the 'closed' signal.

        This handler will notify the declaration object that the popup
        view has closed.

        """
        d = self.declaration
        if d is not None:
            d._popup_closed()

    #--------------------------------------------------------------------------
    # ProxyBubbleView API
    #--------------------------------------------------------------------------
    def set_anchor(self, anchor):
        """ Set the anchor location on the underlying widget.

        """
        self.widget.setAnchor(QPointF(*anchor))

    def set_parent_anchor(self, anchor):
        """ Set the parent anchor location on the underlying widget.

        """
        self.widget.setParentAnchor(QPointF(*anchor))

    def set_arrow_size(self, size):
        """ Set the size of the arrow on the underlying widget.

        """
        self.widget.setArrowSize(size)

    def set_arrow_edge(self, edge):
        """ Set the arrow edge on the underlying widget.

        """
        self.widget.setArrowEdge(EDGES[edge])

    def set_arrow_position(self, pos):
        """ Set the position of the arrow on the underlying widget.

        """
        self.widget.setArrowPosition(pos)

    def set_offset(self, offset):
        """ Set the offset of the underlying widget.

        """
        self.widget.setOffset(QPoint(*offset))

    def set_timeout(self, timeout):
        """ Set the timeout for the underlying widget.

        """
        self.widget.setTimeout(timeout)

    def set_fade_in_duration(self, duration):
        """ Set the fade in duration for the underlying widget.

        """
        self.widget.setFadeInDuration(duration)

    def set_fade_out_duration(self, duration):
        """ Set the fade out duration for the underlying widget.

        """
        self.widget.setFadeOutDuration(duration)

    def close(self):
        """ Close the underlying popup widget.

        """
        self.widget.close()
__author__ = 'IENAC15 - groupe 25'


class Pions(QGraphicsEllipseItem):
    """The view of an aircraft in the GraphicsScene"""

    def __init__(self, moving, f):
        """Plot constructor, creates the ellipse and adds to the scene"""
        super(Pions, self).__init__(None)

        # instance variables
        self.flight = f
        self.moving = moving
        # set color and builds an ellipse
        self.setPen(BLUE_PEN if f.type == traffic.DEP else MAGENTA_PEN)
        self.setBrush(NORMAL_BRUSH)
        self.setRect(-PLOT_SIZE, -PLOT_SIZE,
                     PLOT_SIZE * 2, PLOT_SIZE * 2)
        self.setZValue(PLOT_Z_VALUE)
        # add tooltip
        info = ' '.join([f.callsign, f.type, traffic.to_hms(f.time)])
        self.setToolTip(info)
        self.update_position()
        # connect to ask_inspection_signal in order to toggle_highlight this plot
        self.moving.radarview.ask_inspection_signal.connect(self.toggle_highlight)
        # animate
        # self.anim = self.animation()

        # [TP4]
        self.state_idle = 0
        self.state_dragging = 1
        self.state = self.state_idle
        self.route_item = None

    def animation(self):
        # animate the opacity of the plot to show that the scene changes
        # even if the animation of the traffic is paused by the user
        # QGraphicsItem-s necessitate an Adapter that inherits from QObject
        class Adapter(QObject):
            def __init__(self, item):
                super(Adapter, self).__init__()
                self.item = item

            opacity = pyqtProperty(float, lambda s: s.item.opacity(),
                                   lambda s, v: s.item.setOpacity(v))

        anim = QPropertyAnimation(Adapter(self), b'opacity')
        anim.setDuration(4000)
        anim.setStartValue(0.2)
        anim.setKeyValueAt(0.5, 1)
        anim.setEndValue(0.2)
        anim.setLoopCount(-1)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        # return a reference to keep in order to prevent GC to collect the anim instance
        return anim

    def update_position(self):
        """moves the plot in the scene"""
        coords = self.position_at_time()
        # I could have used *coords as an argument to setPos
        # self.setPos(*coords)
        self.setPos(coords[0], coords[1])

    def position_at_time(self):
        """returns the position of the aircraft at the current time"""
        return self.flight.route[self.moving.radarview.time - self.flight.time]

    @pyqtSlot(traffic.Flight)
    def toggle_highlight(self, flight):
        """ this slot is used to highlights the plot when it's clicked
            and to cancel highlighting when other plots are clicked """
        if flight == self.flight:
            self.setBrush(SELECTED_BRUSH)
        elif self.brush() == SELECTED_BRUSH:
            self.setBrush(NORMAL_BRUSH)

    # ----------------------
    # [TP4]

    def add_flight_route(self):
        path = QPainterPath()
        path.moveTo(*self.flight.route[0])
        for (x, y) in self.flight.route[1:]:
            # print(x,y)
            path.lineTo(x, y)
        item = QGraphicsPathItem(path)
        item.setPen(QPen(QColor(0, 0, 255, 60), 50))
        self.scene().addItem(item)
        return item

    def remove_flight_route(self):
        self.scene().removeItem(self.route_item)

    # interaction

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        event.accept()
        self.moving.radarview.ask_inspection(self.flight)

        self.route_item = self.add_flight_route()
        self.state = self.state_dragging

    def mouseReleaseEvent(self,
                          event):  # reçu même si en dehors de l'item ! spécialité de Qt, qui permet la localité du code
        super().mouseReleaseEvent(event)

        if self.state == self.state_dragging:
            event.accept()
            self.remove_flight_route()
            self.state = self.state_idle

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        if self.state == self.state_dragging:
            event.accept()
            # ce qu'on veut c'est mettre le temps de l'appli au temps correspondant au plot le plus proche du curseur

            # changement de repère : calcul de la position du curseur dans les coordonnées du monde (celles des plots)
            scenePos = self.mapToScene(event.pos())  # du coup l'interaction est insensible au pan and zoom
            (x0, y0) = scenePos.x(), scenePos.y()

            # détermination du temps relatif du plot le plus proche
            import minDist
            minDist_, rminDistTime = minDist.minDist(x0, y0, self.flight.route)
            # minDist, rminDistTime = min((dist, rtime) for (rtime, dist) in enumerate(math.hypot(x-x0,y-y0) for (x,y) in self.flight.route))

            # on change le temps de la scène avec un temps absolu
            self.moving.radarview.set_time(rminDistTime + self.flight.time)

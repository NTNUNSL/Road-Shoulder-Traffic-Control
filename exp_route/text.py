def sumo_conf(k):
    return '<?xml version="1.0" encoding="UTF-8"?>\n\
    <configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">\n\
        <input>\n\
            <net-file value="../../osm.net.xml"/>\n\
            <!--additional-files value="../../osm.poly.xml"/-->\n\
        <route-files value="%s.xml"/>\n\
        </input>\n\
        <processing>\n\
            <ignore-route-errors value="true"/>\n\
        </processing>\n\
        <routing>\n\
            <device.rerouting.adaptation-steps value="180"/>\n\
        </routing>\n\
        <report>\n\
            <verbose value="true"/>\n\
            <duration-log.statistics value="true"/>\n\
            <no-step-log value="true"/>\n\
        </report>\n\
        <gui_only>\n\
            <gui-settings-file value="../../osm.view.xml"/>\n\
        </gui_only>\n\
    </configuration>'%(k)
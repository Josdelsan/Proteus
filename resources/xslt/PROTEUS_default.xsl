<!-- default_template.xsl -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:proteus="http://proteus.lsi.us.es">
    <!-- Match any object -->
    <xsl:template match="object">
        <div>
            <h2>
                <!-- Display the name property as the object title -->
                <xsl:value-of select="properties/stringProperty[@name='name']"/>
            </h2>
            <!-- Render the children objects recursively -->
            <xsl:apply-templates select="children/object"/>
        </div>
    </xsl:template>
</xsl:stylesheet>

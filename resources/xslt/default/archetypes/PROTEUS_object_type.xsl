<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_object_type.xsl                        -->
<!-- Content : PROTEUS XSLT for subjects at US - objective    -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/08/02                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->

<!-- ======================================================== -->
<!-- exclude-result-prefixes="proteus" must be set in all     -->
<!-- files to avoid xmlsn:proteus="." to appear in HTML tags. -->
<!-- ======================================================== -->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    xmlns:proteus-utils="http://proteus.us.es/utils"
    exclude-result-prefixes="proteus proteus-utils"
>

    <!-- ============================================== -->
    <!-- object-type template                           -->
    <!-- ============================================== -->

    <xsl:template match="object[@classes='object-type']">
        <div id="{@id}" data-proteus-id="{@id}" class="object_type">
            <table class="object_type remus_table">

                <!-- Header, version, authors and sources -->
                <xsl:call-template name="generate_software_requirement_expanded_header">
                    <xsl:with-param name="class" select="'objectType'" />
                </xsl:call-template>

                <tr>
                    <td colspan="2">
                        <div class="code">
                            <xsl:apply-templates select="." mode="code"/>
                        </div>
                    </td>
                </tr>

                <!-- Comments -->
                <xsl:call-template name="generate_property_row">
                    <xsl:with-param name="label"   select="$proteus:lang_comments"/>
                    <xsl:with-param name="content" select="properties/markdownProperty[@name='comments']"/>
                </xsl:call-template>

            </table>
        </div>
    </xsl:template>

    <!-- ============================================== -->
    <!-- object-type template (mode code)               -->
    <!-- ============================================== -->

    <xsl:template match="object[@classes='object-type']" mode="code">
        
        <!-- Description -->
        <xsl:call-template name="generate-code-description"/>

        <!-- Class declaration -->
        <xsl:variable name="class_declaration">
            <xsl:choose>
                <xsl:when test="properties/booleanProperty[@name='is-abstract'] = 'true'">abstract class</xsl:when>
                <xsl:otherwise>class</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <xsl:variable name="css_class_declaration">
            <xsl:choose>
                <xsl:when test="properties/booleanProperty[@name='is-abstract'] = 'true'">abstract</xsl:when>
                <xsl:otherwise></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <span class="keyword {$css_class_declaration}">
            <xsl:value-of select="$class_declaration"/>
            <xsl:text> </xsl:text>
        </span>
        <span class="class_name {$css_class_declaration}">
            <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']"/>
        </span>

        <!-- Supertype TODO -->


        <!-- Open bracket -->
        <br></br>
        {
        <br></br>

        <!-- Attributes -->
        <xsl:if test="children/object[@classes='object-attribute']">
            <div class="code_comment code_header"><xsl:value-of select="$proteus:lang_code_attributes"/></div>
            <ul class="properties">
                <xsl:apply-templates select="children/object[@classes='object-attribute']" mode="code"/>
            </ul>
        </xsl:if>

        <br></br>

        <!-- Components -->
        <xsl:if test="children/object[@classes='object-component']">
            <div class="code_comment code_header"><xsl:value-of select="$proteus:lang_code_components"/></div>
            <ul class="properties">
                <xsl:apply-templates select="children/object[@classes='object-component']" mode="code"/>
            </ul>
        </xsl:if>

        <!-- Close bracket -->
        <br></br>
        }

    </xsl:template>

    <!-- ============================================== -->
    <!-- Attribute | Component template                 -->
    <!-- ============================================== -->
    <xsl:template match="object[@classes='object-attribute']" mode="code">
        <li id="{@id}" data-proteus-id="{@id}" class="property">

            <!-- Description -->
            <xsl:call-template name="generate-code-description"/>

            <!-- Keyword -->
            <span class="keyword">
                <xsl:choose>
                    <xsl:when test="properties/enumProperty[@name='kind-of-property'] = 'constant'">const </xsl:when>
                    <xsl:when test="properties/enumProperty[@name='kind-of-property'] = 'variable'">var </xsl:when>
                    <xsl:when test="properties/enumProperty[@name='kind-of-property'] = 'derived'">derived </xsl:when>
                </xsl:choose>
            </span>

            <!-- Name -->
            <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']"/> : 
            <xsl:choose>
                <xsl:when test="properties/enumProperty[@name='type'] = 'set'">Set(</xsl:when>
                <xsl:when test="properties/enumProperty[@name='type'] = 'sequence'">Sequence(</xsl:when>
                <xsl:when test="properties/enumProperty[@name='type'] = 'bag'">Bag(</xsl:when>
            </xsl:choose>

        </li>
    </xsl:template>


    <!-- ============================================== -->
    <!-- Description template                           -->
    <!-- ============================================== -->
    <xsl:template name="generate-code-description">

        <xsl:choose>
            <xsl:when test="string-length(properties/markdownProperty[@name='description']) > 0">
                <div>
                <span class="code_comment">/**</span>
                <br></br>
                <span class="code_comment code_description">
                    <xsl:call-template name="generate_markdown">
                        <xsl:with-param name="content" select="properties/markdownProperty[@name='description']"/>
                    </xsl:call-template>
                </span>
                <span class="code_comment">*/</span>
            </div>
            </xsl:when>
            <xsl:otherwise>
                <br></br>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>


</xsl:stylesheet>
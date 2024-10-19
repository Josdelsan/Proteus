<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_main.xsl                               -->
<!-- Content : PROTEUS default XSLT main file                 -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/06/09                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/08 (Amador Durán)                      -->
<!-- encoding="iso-8859-1" -> enconding="utf-8"               -->
<!-- graphica_file -> local_resource                          -->
<!-- external_resource -> remote_resource                     -->
<!-- archetype_link -> symbolic_link                          -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/13 (Amador Durán)                      -->
<!-- Document loop simplified.                                -->
<!-- Added dictionaries and keys for property and enum labels -->
<!-- Use of EXSLT node-set function to overcome some XLST 1.0 -->
<!-- limitations.                                             -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/14 (Amador Durán)                      -->
<!-- key() does not work on variables in lxml.                -->
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
    xmlns:exsl="http://exslt.org/common"
    extension-element-prefixes="exsl"
>
    <!-- Output -->
    <xsl:output method="html"
        doctype-public="XSLT-compat"
        omit-xml-declaration="yes"
        encoding="utf-8"
        indent="yes"
    />

    <!-- Language independent dictionaries -->
    <!-- NOTE: that would not be necessary in XSLT 2.0, -->
    <!-- where variable names can be computed online    -->

    <!-- PROTEUS property labels dictionary -->
    <xsl:variable name="property_labels_dictionary">
        <label key=":Proteus-date"><xsl:value-of select="$proteus:lang_date"/></label>
        <label key="address"><xsl:value-of select="$proteus:lang_address"/></label>
        <label key="attenders"><xsl:value-of select="$proteus:lang_attenders"/></label>
        <label key="category"><xsl:value-of select="$proteus:lang_category"/></label>
        <label key="comments"><xsl:value-of select="$proteus:lang_comments"/></label>
        <label key="created-by"><xsl:value-of select="$proteus:lang_authors"/></label>
        <label key="date"><xsl:value-of select="$proteus:lang_date"/></label>
        <label key="description"><xsl:value-of select="$proteus:lang_description"/></label>
        <label key="diagram"><xsl:value-of select="$proteus:lang_diagram"/></label>
        <label key="email"><xsl:value-of select="$proteus:lang_email"/></label>
        <label key="importance"><xsl:value-of select="$proteus:lang_importance"/></label>
        <label key="inherits-from"><xsl:value-of select="$proteus:lang_inherits_from"/></label>
        <label key="name"><xsl:value-of select="$proteus:lang_name"/></label>
        <label key="phone-number"><xsl:value-of select="$proteus:lang_telephone"/></label>
        <label key="role"><xsl:value-of select="$proteus:lang_role"/></label>
        <label key="sources"><xsl:value-of select="$proteus:lang_sources"/></label>
        <label key="stability"><xsl:value-of select="$proteus:lang_stability"/></label>
        <label key="version"><xsl:value-of select="$proteus:lang_version"/></label>
        <label key="web"><xsl:value-of select="$proteus:lang_web"/></label>
        <label key="works-for"><xsl:value-of select="$proteus:lang_organization"/></label>
        <label key="status"><xsl:value-of select="$proteus:lang_status"/></label>
        <label key="time"><xsl:value-of select="$proteus:lang_time"/></label>
        <label key="participates-in"><xsl:value-of select="$proteus:lang_participates_in"/></label>
        <label key="place"><xsl:value-of select="$proteus:lang_place"/></label>
        <label key="priority"><xsl:value-of select="$proteus:lang_priority"/></label>
        <label key="results"><xsl:value-of select="$proteus:lang_results"/></label>
    </xsl:variable>

    <!-- This is needed because of limitations of XSLT 1.0 -->
    <!-- Note the use of the node-set() extension function -->
    <!-- Usage: <xsl:value-of select="$property-labels/label[@key=@name])"/> -->
    <xsl:variable name="property_labels" select="exsl:node-set($property_labels_dictionary)"/>

    <!-- Define the key for property labels                           -->
    <!-- WARINIG: it is useless, always returns nothing               -->
    <!-- Using $property_labels/label in key's match is not allowed.  -->
    <!-- Usage: <xsl:value-of select="key('property-label', @name)"/> -->
    <!-- <xsl:key name="property-label" match="label" use="@key"/>    -->

    <!-- PROTEUS enumeration labels dictionary -->
    <xsl:variable name="enum_labels_dictionary">
        <label key="tbd"><xsl:value-of select="$proteus:lang_TBD_expanded"/></label>
        <label key="customer"><xsl:value-of select="$proteus:lang_customer"/></label>
        <label key="developer"><xsl:value-of select="$proteus:lang_developer"/></label>
        <label key="user"><xsl:value-of select="$proteus:lang_user"/></label>
        <label key="critical"><xsl:value-of select="$proteus:lang_critical"/></label>
        <label key="high"><xsl:value-of select="$proteus:lang_high"/></label>
        <label key="medium"><xsl:value-of select="$proteus:lang_medium"/></label>
        <label key="low"><xsl:value-of select="$proteus:lang_low"/></label>
        <label key="optional"><xsl:value-of select="$proteus:lang_optional"/></label>
    </xsl:variable>

    <!-- This is needed because of limitations of XSLT 1.0 -->
    <!-- Note the use of the node-set() extension function -->
    <xsl:variable name="enum_labels" select="exsl:node-set($enum_labels_dictionary)"/>

    <!-- Define the key for enum labels                           -->
    <!-- WARINIG: it is useless, always returns nothing           -->
    <!-- Using $enum_labels/label in key's match is not allowed.  -->
    <!-- Usage: <xsl:value-of select="key('enum-label', @name)"/> -->
    <!-- <xsl:key name="enum-label" match="label" use="@key"/>    -->

    <!-- Template includes -->
    <xsl:include href="PROTEUS_utilities.xsl" />
    <xsl:include href="PROTEUS_properties.xsl" />
    <xsl:include href="PROTEUS_cover.xsl" />
    <xsl:include href="PROTEUS_document.xsl" />

    <xsl:include href="archetypes/general/section.xsl" />
    <xsl:include href="archetypes/general/appendix.xsl" />
    <xsl:include href="archetypes/general/information.xsl" />
    <xsl:include href="archetypes/general/paragraph.xsl" />
    <xsl:include href="archetypes/general/glossary_item.xsl" />
    <xsl:include href="archetypes/general/figure.xsl" />
    <xsl:include href="archetypes/general/organization.xsl" />
    <xsl:include href="archetypes/general/stakeholder.xsl" />
    <xsl:include href="archetypes/general/meeting.xsl" />
    <xsl:include href="archetypes/general/symbolic_link.xsl" />

    <xsl:include href="archetypes/business_analysis/strength.xsl" />
    <xsl:include href="archetypes/business_analysis/weakness.xsl" />
    <xsl:include href="archetypes/business_analysis/business_actor.xsl" />
    <xsl:include href="archetypes/business_analysis/business_process.xsl" />
    <xsl:include href="archetypes/business_analysis/business_objective.xsl" />
    <xsl:include href="archetypes/business_analysis/user_story.xsl" />

    <xsl:include href="archetypes/requirements/subsystem.xsl" />
    <xsl:include href="archetypes/requirements/general-requirement.xsl" />
    <xsl:include href="archetypes/requirements/system-actor.xsl" />
    <xsl:include href="archetypes/requirements/information_requirement.xsl" />
    <xsl:include href="archetypes/requirements/business_rule.xsl" />
    <xsl:include href="archetypes/requirements/functional_requirement.xsl" />
    <xsl:include href="archetypes/requirements/nonfunctional_requirement.xsl" />
    <xsl:include href="archetypes/requirements/traceability_matrix.xsl" />

    <xsl:include href="archetypes/PROTEUS_default.xsl" />

    <!--
    <xsl:include href="archetypes/software/PROTEUS_use_case.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_object_type.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_association_type.xsl" />

    -->

    <xsl:template match="project">
        <xsl:variable name="currentDocumentId" select="proteus-utils:current_document()"/>
        <xsl:apply-templates select="documents/object[@id=$currentDocumentId]"/>
    </xsl:template>

</xsl:stylesheet>
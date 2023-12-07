<?xml version="1.0" encoding="utf-8"?>

<!-- ========================================================= -->
<!-- File    : PROTEUS_i18n_English.xsl                        -->
<!-- Content : PROTEUS XSLT for subjects at US - English i18n  -->
<!--           file                                            -->
<!-- Author  : Amador Durán Toro                               -->
<!--           José María Delgado Sánchez                      -->
<!-- Date    : 2023/06/29                                      -->
<!-- Version : 1.0                                             -->
<!-- ========================================================= -->

<!-- ======================================================== -->
<!-- exclude-result-prefixes="proteus" must be set in all     -->
<!-- files to avoid xmlsn:proteus="." to appear in HTML tags. -->
<!-- ======================================================== -->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    exclude-result-prefixes="proteus"
>

<!-- Same as default in REM 1.2.2 -->
<xsl:variable name="proteus:lang_action">Action</xsl:variable>
<xsl:variable name="proteus:lang_address">Address</xsl:variable>
<xsl:variable name="proteus:lang_alternatives">Alternatives</xsl:variable>
<xsl:variable name="proteus:lang_analysis">Analysis</xsl:variable>
<xsl:variable name="proteus:lang_attenders">Attenders</xsl:variable>
<xsl:variable name="proteus:lang_attribute">Attribute</xsl:variable>
<xsl:variable name="proteus:lang_authors">Authors</xsl:variable>
<xsl:variable name="proteus:lang_average">Average</xsl:variable>
<xsl:variable name="proteus:lang_category">Category</xsl:variable>
<xsl:variable name="proteus:lang_comments">Comments</xsl:variable>
<xsl:variable name="proteus:lang_components">Components</xsl:variable>
<xsl:variable name="proteus:lang_condition">Condition</xsl:variable>
<xsl:variable name="proteus:lang_constant_attribute">Constant attribute</xsl:variable>
<xsl:variable name="proteus:lang_constant_role">Constant rol</xsl:variable>
<xsl:variable name="proteus:lang_date">Date</xsl:variable>
<xsl:variable name="proteus:lang_definition">Definition</xsl:variable>
<xsl:variable name="proteus:lang_dependencies">Dependencies</xsl:variable>
<xsl:variable name="proteus:lang_derived_attribute">Derived attribute</xsl:variable>
<xsl:variable name="proteus:lang_derived_role">Derived role</xsl:variable>
<xsl:variable name="proteus:lang_description">Description</xsl:variable>
<xsl:variable name="proteus:lang_directly_affected_objects">Directly affects</xsl:variable>
<xsl:variable name="proteus:lang_disjoint_subtypes">Subtypes (disjoint)</xsl:variable>
<xsl:variable name="proteus:lang_exception">Exception</xsl:variable>
<xsl:variable name="proteus:lang_exceptions">Exceptions</xsl:variable>
<xsl:variable name="proteus:lang_expected_frequency">Expected frequency</xsl:variable>
<xsl:variable name="proteus:lang_expression">Expression</xsl:variable>
<xsl:variable name="proteus:lang_fax">Fax</xsl:variable>
<xsl:variable name="proteus:lang_figure">Figure</xsl:variable>
<xsl:variable name="proteus:lang_freelance">Freelance</xsl:variable>
<xsl:variable name="proteus:lang_if">If</xsl:variable>
<xsl:variable name="proteus:lang_indirectly_affected_objects">Indirectly affects</xsl:variable>
<xsl:variable name="proteus:lang_invariant">Invariant expression</xsl:variable>
<xsl:variable name="proteus:lang_importance">Importance</xsl:variable>
<xsl:variable name="proteus:lang_initialValue">Initial value</xsl:variable>
<xsl:variable name="proteus:lang_isCustomer">Is customer</xsl:variable>
<xsl:variable name="proteus:lang_isDeveloper">Is developer</xsl:variable>
<xsl:variable name="proteus:lang_isUser">Is user</xsl:variable>
<xsl:variable name="proteus:lang_lifetime">Lifetime</xsl:variable>
<xsl:variable name="proteus:lang_maximum">Maximum</xsl:variable>
<xsl:variable name="proteus:lang_maximum_time">Maximum time</xsl:variable>
<xsl:variable name="proteus:lang_meeting">Meeting</xsl:variable>
<xsl:variable name="proteus:lang_multiplicity">Multiplicity</xsl:variable>
<xsl:variable name="proteus:lang_name">Name</xsl:variable>
<xsl:variable name="proteus:lang_no">No</xsl:variable>
<xsl:variable name="proteus:lang_none">None</xsl:variable>
<xsl:variable name="proteus:lang_OCL_condition">Condition (OCL)</xsl:variable>
<xsl:variable name="proteus:lang_OCL_expression">OCL expression</xsl:variable>
<xsl:variable name="proteus:lang_OCL_postconditions">Postcondition expressions (OCL)</xsl:variable>
<xsl:variable name="proteus:lang_OCL_preconditions">Precondition expressions (OCL)</xsl:variable>
<xsl:variable name="proteus:lang_ordinary_sequence">Ordinary sequence</xsl:variable>
<xsl:variable name="proteus:lang_organization">Organization</xsl:variable>
<xsl:variable name="proteus:lang_overlapping_subtypes">Subtypes (overlapping)</xsl:variable>
<xsl:variable name="proteus:lang_parameters">Parameters</xsl:variable>
<xsl:variable name="proteus:lang_performance">Performance</xsl:variable>
<xsl:variable name="proteus:lang_place">Place</xsl:variable>
<xsl:variable name="proteus:lang_possible_solution">Possible solution</xsl:variable>
<xsl:variable name="proteus:lang_postcondition">Postcondition</xsl:variable>
<xsl:variable name="proteus:lang_postconditions">Postcondition expressions</xsl:variable>
<xsl:variable name="proteus:lang_precondition">Precondition</xsl:variable>
<xsl:variable name="proteus:lang_preconditions">Precondition expressions</xsl:variable>
<xsl:variable name="proteus:lang_prepared_by">Prepared by:</xsl:variable>
<xsl:variable name="proteus:lang_prepared_for">Prepared for:</xsl:variable>
<xsl:variable name="proteus:lang_project">Project</xsl:variable>
<xsl:variable name="proteus:lang_related_objectives">Traced-to objectives</xsl:variable>
<xsl:variable name="proteus:lang_related_requirements">Traced-to requirements</xsl:variable>
<xsl:variable name="proteus:lang_result_type">Result type</xsl:variable>
<xsl:variable name="proteus:lang_results">Results</xsl:variable>
<xsl:variable name="proteus:lang_role">Role</xsl:variable>
<xsl:variable name="proteus:lang_simultaneous_ocurrences">Simultaneous ocurrences</xsl:variable>
<xsl:variable name="proteus:lang_sources">Sources</xsl:variable>
<xsl:variable name="proteus:lang_specific_data">Specific data</xsl:variable>
<xsl:variable name="proteus:lang_stability">Stability</xsl:variable>
<xsl:variable name="proteus:lang_stakeholder">Stakeholder</xsl:variable>
<xsl:variable name="proteus:lang_status">Status</xsl:variable>
<xsl:variable name="proteus:lang_step">Step</xsl:variable>
<xsl:variable name="proteus:lang_subobjectives">Subobjectives</xsl:variable>
<xsl:variable name="proteus:lang_subtypes">Subtypes</xsl:variable>
<xsl:variable name="proteus:lang_supertype">Supertype</xsl:variable>
<xsl:variable name="proteus:lang_system">system</xsl:variable>
<xsl:variable name="proteus:lang_TBD">TBD</xsl:variable>
<xsl:variable name="proteus:lang_telephone">Telephone</xsl:variable>
<xsl:variable name="proteus:lang_The">The</xsl:variable>
<xsl:variable name="proteus:lang_the">the</xsl:variable>
<xsl:variable name="proteus:lang_The_actor">Actor</xsl:variable>
<xsl:variable name="proteus:lang_the_actor">actor</xsl:variable>
<xsl:variable name="proteus:lang_then_this_use_case">then this use case</xsl:variable>
<xsl:variable name="proteus:lang_time">Time</xsl:variable>
<xsl:variable name="proteus:lang_times_per">times per</xsl:variable>
<xsl:variable name="proteus:lang_TOC">Table of contents</xsl:variable>
<xsl:variable name="proteus:lang_traceability_matrix">Traceability matrix</xsl:variable>
<xsl:variable name="proteus:lang_type">Type</xsl:variable>
<xsl:variable name="proteus:lang_urgency">Urgency</xsl:variable>
<xsl:variable name="proteus:lang_variable_attribute">Variable attribute</xsl:variable>
<xsl:variable name="proteus:lang_variable_role">Variable role</xsl:variable>
<xsl:variable name="proteus:lang_version">Version</xsl:variable>
<xsl:variable name="proteus:lang_yes">Yes</xsl:variable>

<!-- new in PROTEUS -->
<xsl:variable name="proteus:lang_code_attributes">// attributes</xsl:variable>
<xsl:variable name="proteus:lang_code_components">// components</xsl:variable>
<xsl:variable name="proteus:lang_code_invariants">// invariants</xsl:variable>
<xsl:variable name="proteus:lang_code_roles">// roles</xsl:variable>
<xsl:variable name="proteus:lang_code_preconditions">// preconditions</xsl:variable>
<xsl:variable name="proteus:lang_code_postconditions">// postconditions</xsl:variable>
<xsl:variable name="proteus:lang_code_exception">exception</xsl:variable>
<xsl:variable name="proteus:lang_code_exceptions">// exceptions</xsl:variable>

<!-- ================== -->
<!-- General L-patterns -->
<!-- ================== -->

<xsl:variable name="proteus:lang_the_system_shall">The system shall</xsl:variable>
<xsl:variable name="proteus:lang_TBD_expanded">To be determined</xsl:variable>

<!-- ===================== -->
<!-- L-patterns for actors -->
<!-- ===================== -->

<xsl:variable name="proteus:lang_this_actor_represents">This actor represents</xsl:variable>

<!-- ======================================= -->
<!-- L-patterns for information requirements -->
<!-- ======================================= -->

<xsl:variable name="proteus:lang_irq_lp_01">The system shall store the information corresponding to</xsl:variable>

<xsl:variable name="proteus:lang_irq_lp_02">More specifically:</xsl:variable>

<!-- ======================================= -->
<!-- L-patterns for constraint requirements  -->
<!-- ======================================= -->

<xsl:variable name="proteus:lang_crq_lp_01">The system shall be compliant with the following business rule or constraint:</xsl:variable>

<!-- ======================== -->
<!-- L-patterns for use cases -->
<!-- ======================== -->

<xsl:variable name="proteus:lang_uc_lp_01">The system shall behave as described in the following</xsl:variable>

<xsl:variable name="proteus:lang_uc_lp_02">abstract use case during the performance of the following use cases:</xsl:variable>

<xsl:variable name="proteus:lang_uc_lp_03">use case when</xsl:variable>

<xsl:variable name="proteus:lang_uc_lp_04">or during the performance of the following use cases:</xsl:variable>

<xsl:variable name="proteus:lang_uc_lp_05">Use case</xsl:variable>

<xsl:variable name="proteus:lang_uc_lp_06">use case</xsl:variable>

<xsl:variable name="proteus:lang_uc_lp_07">is performed</xsl:variable>

<!-- =========================== -->
<!-- L-patterns for object types -->
<!-- =========================== -->

<xsl:variable name="proteus:lang_ot_lp_01">This object type represents</xsl:variable>

<xsl:variable name="proteus:lang_ot_lp_02">This abstract object type represents</xsl:variable>

<!-- ================================ -->
<!-- L-patterns for association types -->
<!-- ================================ -->

<xsl:variable name="proteus:lang_at_lp_01">This association type represents the fact that</xsl:variable>

<!-- =========================== -->
<!-- L-patterns for value types  -->
<!-- =========================== -->

<xsl:variable name="proteus:lang_vt_lp_01">This value type represents</xsl:variable>

<!-- ========================= -->
<!-- L-patterns for attributes -->
<!-- ========================= -->

<xsl:variable name="proteus:lang_att_lp_01">This attribute represents</xsl:variable>

<!-- ==================== -->
<!-- L-patterns for roles -->
<!-- ==================== -->

<xsl:variable name="proteus:lang_role_lp_01">This role represents</xsl:variable>

</xsl:stylesheet>

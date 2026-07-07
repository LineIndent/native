---
title: "Native Select"
description: "A styled native HTML select element with consistent design system integration."
order: 0
---

--DEMO(native_accordion_demo)--
--DEMO(exclusive_accordion_demo)--
--DEMO(native_switch_demo)--


# Native Select

A styled native HTML select element with consistent design system integration.

# Installation

Copy the following code into your app directory.

--INSTALL(native_select)--

# Usage

--USAGE(native_select)--

# Anatomy 
Use the following composition to build a `Native Select` component.

--ANATOMY(native_select)--

# Examples

## Basic

--DEMO(native_select_basic)--

## Groups

Use `native_select.optgroup` to organize options into categories.

--DEMO(native_select_groups)--

## Disabled

Add the `disabled` prop to the `native_select` component to disable the select.

--DEMO(native_select_disabled)--

## Invalid

Use `aria-invalid` to show validation errors and the `data-invalid` attribute to the `field` component for styling.

--DEMO(native_select_invalid)--

# API Reference

Here is the converted documentation rewritten to match your custom Python Reflex `native_select` API layout:

## native_select

The main select component that wraps the native HTML select element.

```python
native_select(
    native_select.option("Option 1", value="option1"),
    native_select.option("Option 2", value="option2"),
)
```

## native_select.option

Represents an individual option within the select.

| Prop | Type | Default |
| --- | --- | --- |
| `value` | `str` |  |
| `disabled` | `bool` | `False` |

## native_select.optgroup

Groups related options together for better organization.

| Prop | Type | Default |
| --- | --- | --- |
| `label` | `str` |  |
| `disabled` | `bool` | `False` |

```python
native_select.optgroup(
    native_select.option("Apple", value="apple"),
    native_select.option("Banana", value="banana"),
    label="Fruits",
)
```

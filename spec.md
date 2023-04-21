# Title: Software Requirements Specifications for an Odoo-based Photovoltaic Installation Management System

## 1. Introduction
### 1.1 Purpose
This document describes the software requirements specifications for an Odoo-based solution designed to streamline the process of transferring customer requirements in photovoltaic installation companies from the sales stage to the project stage. The solution will use the free Form Builder module from the Odoo App Store and include built-in plausibility checks, communication between sales and project managers, and data consistency across modules.

### 1.2 Scope
The scope of this document is limited to the identification of required modules, features, and functionalities for the Odoo-based solution, applicable to Odoo version 15.

## 2. System Overview
The system will be composed of several Odoo modules, including:

- Form Builder Module ([Available from AppStore](https://apps.odoo.com/apps/modules/15.0/formio/))
- CRM Module (Standard Odoo)
- Projects Module (Standard Odoo)
- ~Communication Module~
- Plausibility Check Module
- Data Integration Module

## 3. Modules and Functionalities
### 3.1 Form Builder Module

[Available from AppStore](https://apps.odoo.com/apps/modules/15.0/formio/)

The Form Builder Module will be used to create custom forms for capturing customer requirements during the pre-sales phase. The module will ensure that the collected data is compatible with both the Sales Module and Projects Module.

### 3.2 CRM Module
This module will manage the pre-sales activities, including the collection of customer requirements using the forms created in the Form Builder Module. The information collected in this module will be passed on to the Projects Module after passing plausibility checks.

Provide a button on the CRM > Opportunity view to launch the CRM-Form for a sales user.

The data collected by Salesperson on a CRM-Opp on a form (generated on FormBuilder) is stored on a separate Odoo model (not crm.lead, not project.project). This model is accessible from other Odoo modules like CRM, Project etc.

### 3.3 Projects Module
This standard Odoo module will be responsible for managing the project activities after the successful transfer of customer requirements from the Sales Module. Project managers will review the data and communicate with salespeople for any clarification needed.

- If certain fields are missing or improperly filled by Salespeople, a PM can "return them to CRM" and seek clarifications. 
- This happens by changing the status of the dataset to "Sales Revision". 
- A message is posted in the CRM-Chatter, and an Activity is posted for the Salesperson with a list of missing items as a checkbox list. 
- PM is able to mark the fields that are missing or incorrectly filled out (which are listed in the Salesperson's Activity list).

### 3.4 Link via SaleOrder
There is a one-to-one relationship between a CRM-Opp and a Project, connected via SaleOrder.

![2023-04-21_18-05-29](https://user-images.githubusercontent.com/7826363/233683275-98277952-046b-418c-81a8-1d803932ab0e.png)


### 3.5 Plausibility Check Module
This module will validate customer requirements collected in the pre-sales phase by performing plausibility checks. Only validated data will be allowed to be transferred to the Projects Module. It is possible to describe the fields in FormBuilder, while marking them as mandatory or not.

### 3.6 Data Integration Module
This module will ensure that the data collected by the Form Builder Module is consistent and compatible between the Sales Module and the Projects Module. Consider the 3 options of:

- Adding fields to CRM model
- Adding fields to Projects model
- Creating a completely new model in which the FormBuilder inputs are managed.

## 4. External Interfaces
The Odoo-based solution will use Odoo version 15's API to communicate with other systems and services, as well as to ensure compatibility with the existing Odoo infrastructure.

## 5. Non-functional Requirements
### 5.1 Performance
The solution must provide efficient data transfer between the Sales Module and Projects Module, minimizing latency during communication between salespeople and project managers.

### 5.2 Security
The system must adhere to Odoo version 15's security standards, ensuring the protection of sensitive customer information and company data.

Only Admin can create, edit and deactivate/delete a form.

### 5.3 Scalability
The solution must be scalable to accommodate the growth of the photovoltaic installation company, including handling increased data volume and user load.

### 5.4 Maintainability
The system should be easily maintainable, allowing for updates and enhancements without disrupting existing functionality.

## 6. Conclusion
This document outlines the software requirements for an Odoo-based solution that will streamline the process of transferring customer requirements from the sales stage to the project stage in photovoltaic installation companies. The solution will use various interconnected modules to facilitate communication, data validation, and data consistency.

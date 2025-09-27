import { BaseTabRenderer } from './BaseTabRenderer';
import { ComprehensiveInstrumentData } from '../../types/api';
import { formatDate } from '../../utils/helpers';
import { formatLeiStatus, getLeiStatusBadgeClass } from '../../utils/formatters/dataFormatters';

export class LeiTabRenderer extends BaseTabRenderer {
  getTabId(): string {
    return 'lei';
  }

  getTabLabel(): string {
    return 'Legal Entity';
  }

  isEnabled(data: ComprehensiveInstrumentData): boolean {
    const leiId = data.instrument?.lei_id || data.instrument?.lei || data.instrument?.legal_entity_identifier;
    return !!leiId || !!data.lei_data;
  }

  render(data: ComprehensiveInstrumentData): string {
    const { instrument, lei_data, relationships } = data;
    const leiId = instrument?.lei_id || instrument?.lei || instrument?.legal_entity_identifier;
    
    console.log('LEI Tab Renderer - instrument:', instrument);
    console.log('LEI Tab Renderer - lei_data:', lei_data);
    console.log('LEI Tab Renderer - relationships:', relationships);
    console.log('LEI Tab Renderer - leiId:', leiId);
    
    if (!leiId && !lei_data) {
      return this.renderNoDataState(
        'No LEI Information',
        'This instrument does not have an associated Legal Entity Identifier (LEI)'
      );
    }

    return `
      <div class="space-y-6">
        <!-- LEI Details -->
        <div class="bg-gray-50 rounded-lg p-4">
          ${this.renderSectionHeader('Legal Entity Information')}
          ${this.renderLeiBasicInfo(instrument, lei_data)}
        </div>

        <!-- Addresses -->
        ${lei_data?.addresses ? this.renderAddressSection(lei_data) : ''}

        <!-- Registration Details -->
        ${lei_data?.registration ? this.renderRegistrationSection(lei_data) : ''}

        <!-- Corporate Structure -->
        ${relationships ? this.renderCorporateStructure(relationships) : ''}
      </div>
    `;
  }

  private renderLeiBasicInfo(instrument: any, lei_data: any): string {
    const basicInfo = [
      { label: 'LEI', value: instrument.lei_id || lei_data?.lei, isCode: true }
    ];

    if (lei_data) {
      // Add fields that actually exist in the API response
      if (lei_data.name) {
        basicInfo.push({ label: 'Entity Name', value: lei_data.name, isCode: false });
      }
      if (lei_data.jurisdiction) {
        basicInfo.push({ label: 'Jurisdiction', value: lei_data.jurisdiction, isCode: false });
      }
      if (lei_data.legal_form) {
        basicInfo.push({ label: 'Legal Form', value: lei_data.legal_form, isCode: false });
      }

      // Add optional fields only if they exist
      if (lei_data.registered_as) {
        basicInfo.push({ label: 'Registered As', value: lei_data.registered_as, isCode: false });
      }
      if (lei_data.managing_lou) {
        basicInfo.push({ label: 'Managing LOU', value: lei_data.managing_lou, isCode: false });
      }
      if (lei_data.bic) {
        basicInfo.push({ label: 'BIC', value: lei_data.bic, isCode: true });
      }
      if (lei_data.next_renewal_date) {
        basicInfo.push({ label: 'Next Renewal', value: formatDate(lei_data.next_renewal_date), isCode: false });
      }
    }

    let content = `
      <dl class="grid grid-cols-1 md:grid-cols-2 gap-4">
        ${basicInfo.map(item => this.renderDefinitionItem(item.label, item.value, item.isCode)).join('')}
    `;

    if (lei_data?.status) {
      content += `
        <div class="flex justify-between">
          <dt class="text-sm font-medium text-gray-500">Status</dt>
          <dd class="text-sm text-gray-900">
            ${this.renderStatusBadge(formatLeiStatus(lei_data.status), getLeiStatusBadgeClass(lei_data.status))}
          </dd>
        </div>
      `;
    }

    // Add information about missing data sections
    const missingSections = [];
    if (!lei_data?.addresses?.length) missingSections.push('Address information');
    if (!lei_data?.registration) missingSections.push('Registration details');
    
    if (missingSections.length > 0) {
      content += `
        <div class="md:col-span-2 p-3 bg-yellow-50 border border-yellow-200 rounded">
          <div class="text-sm text-yellow-800">
            <strong>Note:</strong> ${missingSections.join(' and ')} not available in the database
          </div>
        </div>
      `;
    }

    if (!lei_data) {
      content += '<div class="col-span-2 text-sm text-gray-500">LEI details not available</div>';
    }

    content += '</dl>';
    return content;
  }

  private renderAddressSection(lei_data: any): string {
    console.log('LEI addresses data:', lei_data?.addresses);
    if (!lei_data?.addresses?.length) {
      return '<div class="text-sm text-gray-500 p-4">No address information available</div>';
    }

    return `
      <div class="bg-blue-50 rounded-lg p-4">
        ${this.renderSectionHeader('Addresses')}
        <div class="space-y-3">
          ${lei_data.addresses.map((address: any) => this.renderAddress(address)).join('')}
        </div>
      </div>
    `;
  }

  private renderAddress(address: any): string {
    return `
      <div class="bg-white rounded p-3">
        <div class="flex justify-between items-start mb-2">
          <h4 class="text-sm font-medium text-gray-700">${address.type || 'Address'}</h4>
          <span class="text-xs text-gray-500">${address.country || ''}</span>
        </div>
        <div class="text-sm text-gray-600">
          ${address.address_lines ? `<div>${address.address_lines}</div>` : ''}
          ${address.city ? `<div>${address.city}${address.region ? `, ${address.region}` : ''}</div>` : ''}
          ${address.postal_code ? `<div>${address.postal_code}</div>` : ''}
        </div>
      </div>
    `;
  }

  private renderRegistrationSection(lei_data: any): string {
    console.log('LEI registration data:', lei_data?.registration);
    if (!lei_data?.registration) {
      return '<div class="text-sm text-gray-500 p-4">No registration information available</div>';
    }

    const registration = lei_data.registration;
    const registrationInfo = [
      { label: 'Registration Status', value: registration.status },
      { label: 'Last Update', value: registration.last_update ? formatDate(registration.last_update) : 'N/A' },
      { label: 'Initial Date', value: registration.initial_date ? formatDate(registration.initial_date) : 'N/A' },
      { label: 'Next Renewal', value: registration.next_renewal ? formatDate(registration.next_renewal) : 'N/A' }
    ];

    return `
      <div class="bg-green-50 rounded-lg p-4">
        ${this.renderSectionHeader('Registration Details')}
        <dl class="grid grid-cols-1 md:grid-cols-2 gap-4">
          ${registrationInfo.map(item => this.renderDefinitionItem(item.label, item.value)).join('')}
          ${registration.validation_sources ? `
            <div class="md:col-span-2">
              ${this.renderDefinitionItem('Validation Sources', registration.validation_sources)}
            </div>
          ` : ''}
        </dl>
      </div>
    `;
  }

  private renderCorporateStructure(relationships: any): string {
    console.log('Corporate structure data:', relationships);
    console.log('Corporate structure type:', typeof relationships);
    console.log('Corporate structure keys:', relationships ? Object.keys(relationships) : 'null');
    
    if (!relationships) {
      return `
        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div class="text-sm text-yellow-800">
            <strong>Corporate Structure:</strong> No relationship data available in the database
          </div>
        </div>
      `;
    }

    // Handle the actual API response structure: {entity: {...}, relationships: [...]}
    const relationshipList = relationships.relationships || [];
    const currentEntity = relationships.entity || {};
    
    if (!relationshipList || relationshipList.length === 0) {
      return `
        <div class="bg-purple-50 rounded-lg p-4">
          ${this.renderSectionHeader('Corporate Structure')}
          <div class="bg-white rounded-lg p-4 border border-gray-200">
            <div class="text-center text-sm text-gray-600">
              <div class="mb-2">
                <strong>${currentEntity.name || 'Current Entity'}</strong>
              </div>
              <div class="text-xs text-gray-500 font-mono">${currentEntity.lei || 'No LEI'}</div>
              <div class="mt-2 text-gray-500">No corporate relationships found</div>
            </div>
          </div>
        </div>
      `;
    }

    return `
      <div class="bg-purple-50 rounded-lg p-4">
        ${this.renderSectionHeader('Corporate Structure')}
        <div class="space-y-6">
          <div class="bg-white rounded-lg p-4 border border-gray-200">
            <div class="space-y-3">
              ${this.renderRelationshipHierarchy(relationships)}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  private renderRelationshipHierarchy(relationships: any): string {
    let hierarchy = '';
    
    const relationshipList = relationships.relationships || [];
    const currentEntity = relationships.entity || {};
    
    console.log('Relationship list:', relationshipList);
    console.log('Current entity:', currentEntity);

    // Group relationships by role - check if current entity is parent or child
    const currentEntityLei = currentEntity.lei;
    
    const parentRelationships = relationshipList.filter((rel: any) => 
      rel.child_lei === currentEntityLei && rel.relationship_status === 'ACTIVE'
    );
    
    const childRelationships = relationshipList.filter((rel: any) => 
      rel.parent_lei === currentEntityLei && rel.relationship_status === 'ACTIVE'
    );

    console.log('Parent relationships:', parentRelationships);
    console.log('Child relationships:', childRelationships);

    // Render parent relationships (entities that own this entity)
    if (parentRelationships.length > 0) {
      parentRelationships.forEach((parent: any) => {
        const parentEntity = {
          lei: parent.parent_lei,
          name: parent.parent_name,
          jurisdiction: parent.parent_jurisdiction
        };
        hierarchy += this.renderEntityCard(parentEntity, 'Parent Company', 'green');
        hierarchy += this.renderConnectionLine();
      });
    }

    // Current Entity (center)
    hierarchy += `
      <div class="flex items-center text-sm">
        <div class="flex-shrink-0 w-4 h-4 mr-3">
          <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 2L3 7v11a1 1 0 001 1h12a1 1 0 001-1V7l-7-5z"/>
          </svg>
        </div>
        <div class="bg-gray-100 rounded-lg p-3 flex-1 border-2 border-gray-400">
          <div class="font-medium text-gray-900">${currentEntity.name || 'Current Entity'}</div>
          <div class="text-xs text-gray-700 font-mono">${currentEntity.lei || 'This Entity'}</div>
          <div class="text-xs text-gray-600">${currentEntity.jurisdiction || ''}</div>
        </div>
      </div>
    `;

    // Render child relationships (entities owned by this entity)
    if (childRelationships.length > 0) {
      hierarchy += this.renderConnectionLine();
      hierarchy += `
        <div class="space-y-2">
          <div class="text-xs text-gray-600 font-medium px-2">Subsidiaries (${childRelationships.length})</div>
      `;
      
      childRelationships.forEach((child: any, index: number) => {
        const childEntity = {
          lei: child.child_lei,
          name: child.child_name,
          jurisdiction: child.child_jurisdiction
        };
        hierarchy += this.renderEntityCard(childEntity, 'Subsidiary', 'orange');
        
        // Add connection line between subsidiaries (except for the last one)
        if (index < childRelationships.length - 1) {
          hierarchy += '<div class="ml-6"><div class="w-px h-2 bg-gray-200"></div></div>';
        }
      });
      
      hierarchy += '</div>';
    }

    return hierarchy;
  }

  private renderEntityCard(entity: any, type: string, color: string): string {
    if (!entity) {
      return `
        <div class="flex items-center text-sm">
          <div class="flex-shrink-0 w-4 h-4 mr-3">
            <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"/>
            </svg>
          </div>
          <div class="bg-gray-100 rounded-lg p-3 flex-1">
            <div class="font-medium text-gray-900">Unknown Entity</div>
            <div class="text-xs text-gray-600">${type}</div>
          </div>
        </div>
      `;
    }
    
    // Handle TailwindCSS class names properly for dynamic colors
    const bgColor = color === 'green' ? 'bg-green-100' : 
                   color === 'orange' ? 'bg-orange-100' : 
                   color === 'blue' ? 'bg-blue-100' : 'bg-gray-100';
    
    const nameColor = color === 'green' ? 'text-green-900' : 
                     color === 'orange' ? 'text-orange-900' : 
                     color === 'blue' ? 'text-blue-900' : 'text-gray-900';
    
    const leiColor = color === 'green' ? 'text-green-700' : 
                    color === 'orange' ? 'text-orange-700' : 
                    color === 'blue' ? 'text-blue-700' : 'text-gray-700';
    
    const typeColor = color === 'green' ? 'text-green-600' : 
                     color === 'orange' ? 'text-orange-600' : 
                     color === 'blue' ? 'text-blue-600' : 'text-gray-600';
    
    return `
      <div class="flex items-center text-sm">
        <div class="flex-shrink-0 w-4 h-4 mr-3">
          <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"/>
          </svg>
        </div>
        <div class="${bgColor} rounded-lg p-3 flex-1">
          <div class="font-medium ${nameColor}">${entity.name || 'Unknown Entity'}</div>
          <div class="text-xs ${leiColor} font-mono">${entity.lei || 'No LEI'}</div>
          <div class="text-xs ${typeColor}">${entity.jurisdiction || 'Unknown'} • ${type}</div>
        </div>
      </div>
    `;
  }

  private renderConnectionLine(): string {
    return `
      <div class="flex justify-center">
        <div class="w-px h-4 bg-gray-300"></div>
      </div>
    `;
  }
}

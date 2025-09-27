import { BaseTabRenderer } from './BaseTabRenderer';
import { ComprehensiveInstrumentData } from '../../types/api';

export class CfiTabRenderer extends BaseTabRenderer {
  getTabId(): string {
    return 'cfi';
  }

  getTabLabel(): string {
    return 'CFI Classification';
  }

  isEnabled(data: ComprehensiveInstrumentData): boolean {
    return !!(data.instrument?.cfi_code || data.instrument?.cfi);
  }

  render(data: ComprehensiveInstrumentData): string {
    const { instrument } = data;
    const cfiCode = instrument?.cfi_code || instrument?.cfi;
    
    if (!cfiCode) {
      return this.renderNoDataState(
        'No CFI Code',
        'This instrument does not have a Classification of Financial Instruments (CFI) code'
      );
    }
    const cfiBreakdown = this.parseCfiCode(cfiCode);

    return `
      <div class="space-y-6">
        <!-- CFI Code Header -->
        <div class="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6">
          ${this.renderSectionHeader('CFI Code Analysis')}
          <div class="text-center">
            <div class="text-3xl font-bold font-mono text-gray-900 mb-2">${cfiCode}</div>
            <div class="text-lg text-gray-600">${cfiBreakdown.description}</div>
          </div>
        </div>

        <!-- CFI Breakdown -->
        <div class="bg-white rounded-lg border border-gray-200 p-6">
          ${this.renderSectionHeader('Code Breakdown')}
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            ${this.renderCfiPositions(cfiBreakdown)}
          </div>
        </div>

        <!-- Additional Information -->
        <div class="bg-blue-50 rounded-lg p-4">
          ${this.renderSectionHeader('About CFI Codes')}
          <p class="text-sm text-gray-700">
            The Classification of Financial Instruments (CFI) code is an international standard (ISO 10962) 
            that provides a standardized method for classifying financial instruments. The 6-character code 
            describes the instrument type, attributes, and specific characteristics.
          </p>
        </div>
      </div>
    `;
  }

  private parseCfiCode(cfiCode: string): any {
    if (!cfiCode || cfiCode.length !== 6) {
      return {
        description: 'Invalid CFI Code',
        positions: []
      };
    }

    const positions = [
      { position: 1, character: cfiCode[0], label: 'Category', description: this.getCfiCategory(cfiCode[0]) },
      { position: 2, character: cfiCode[1], label: 'Group', description: this.getCfiGroup(cfiCode[0], cfiCode[1]) },
      { position: 3, character: cfiCode[2], label: 'Attribute 1', description: this.getCfiAttribute(cfiCode[0], 2, cfiCode[2]) },
      { position: 4, character: cfiCode[3], label: 'Attribute 2', description: this.getCfiAttribute(cfiCode[0], 3, cfiCode[3]) },
      { position: 5, character: cfiCode[4], label: 'Attribute 3', description: this.getCfiAttribute(cfiCode[0], 4, cfiCode[4]) },
      { position: 6, character: cfiCode[5], label: 'Attribute 4', description: this.getCfiAttribute(cfiCode[0], 5, cfiCode[5]) }
    ];

    return {
      description: this.getInstrumentDescription(cfiCode),
      positions
    };
  }

  private renderCfiPositions(cfiBreakdown: any): string {
    return cfiBreakdown.positions.map((pos: any) => `
      <div class="bg-gray-50 rounded-lg p-4">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-500">Position ${pos.position}</span>
          <span class="text-2xl font-bold font-mono text-purple-600">${pos.character}</span>
        </div>
        <div class="text-sm font-medium text-gray-900 mb-1">${pos.label}</div>
        <div class="text-sm text-gray-600">${pos.description}</div>
      </div>
    `).join('');
  }

  private getCfiCategory(char: string): string {
    const categories: Record<string, string> = {
      'E': 'Equities',
      'D': 'Debt instruments',
      'R': 'Rights',
      'O': 'Options',
      'F': 'Futures',
      'S': 'Swaps',
      'H': 'Non-listed and complex listed options',
      'I': 'Others (miscellaneous)',
      'J': 'Referential instruments',
      'K': 'Structured instruments',
      'L': 'Strategy instruments',
      'M': 'Financing instruments'
    };
    return categories[char] || 'Unknown category';
  }

  private getCfiGroup(category: string, group: string): string {
    const groups: Record<string, Record<string, string>> = {
      'E': {
        'S': 'Common/ordinary shares',
        'P': 'Preferred/preference shares',
        'C': 'Convertible shares',
        'F': 'Preference shares (with warrants)',
        'V': 'Preference shares (convertible)',
        'R': 'Preferred/preference shares (redeemable)',
        'L': 'Limited partnership units',
        'M': 'Others (miscellaneous)'
      }
    };
    return groups[category]?.[group] || `Group ${group}`;
  }

  private getCfiAttribute(_category: string, _position: number, char: string): string {
    // Simplified attribute mapping - in a real implementation, 
    // this would be much more comprehensive
    if (char === 'N') return 'Not applicable/undefined';
    return `Attribute value: ${char}`;
  }

  private getInstrumentDescription(cfiCode: string): string {
    const category = cfiCode[0];
    const group = cfiCode[1];
    
    if (category === 'E' && group === 'S') {
      return 'Common/Ordinary Share';
    }
    
    return `${this.getCfiCategory(category)} - ${this.getCfiGroup(category, group)}`;
  }
}

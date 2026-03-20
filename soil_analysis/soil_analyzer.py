"""
Soil Fertility Analysis Module
Analyzes NPK values and determines fertility status
"""


class SoilAnalyzer:
    """Analyzes soil fertility based on NPK values"""
    
    # Thresholds for NPK values (mg/kg or ppm)
    THRESHOLDS = {
        'NITROGEN': {
            'LOW': 20,
            'MEDIUM': 40,
            'HIGH': 100
        },
        'PHOSPHORUS': {
            'LOW': 10,
            'MEDIUM': 20,
            'HIGH': 50
        },
        'POTASSIUM': {
            'LOW': 100,
            'MEDIUM': 200,
            'HIGH': 400
        }
    }
    
    def __init__(self):
        """Initialize soil analyzer"""
        pass
    
    def analyze(self, nitrogen, phosphorus, potassium):
        """
        Analyze soil fertility based on NPK values
        
        Args:
            nitrogen: Nitrogen value (N)
            phosphorus: Phosphorus value (P)
            potassium: Potassium value (K)
            
        Returns:
            Dictionary containing analysis results
        """
        # Determine status for each nutrient
        n_status = self._get_status(nitrogen, 'NITROGEN')
        p_status = self._get_status(phosphorus, 'PHOSPHORUS')
        k_status = self._get_status(potassium, 'POTASSIUM')
        
        # Overall fertility status (based on average)
        avg_value = (nitrogen + phosphorus + potassium) / 3
        overall_status = self._get_overall_status(avg_value, nitrogen, phosphorus, potassium)
        
        # Detect nutrient imbalances
        imbalances = []
        if n_status == 'LOW':
            imbalances.append('LOW_NITROGEN')
        if p_status == 'LOW':
            imbalances.append('LOW_PHOSPHORUS')
        if k_status == 'LOW':
            imbalances.append('LOW_POTASSIUM')
        
        return {
            'nitrogen': {
                'value': float(nitrogen),
                'status': n_status
            },
            'phosphorus': {
                'value': float(phosphorus),
                'status': p_status
            },
            'potassium': {
                'value': float(potassium),
                'status': k_status
            },
            'overall_status': overall_status,
            'imbalances': imbalances
        }
    
    def _get_status(self, value, nutrient):
        """
        Get status for a single nutrient
        
        Args:
            value: Nutrient value
            nutrient: Nutrient name ('NITROGEN', 'PHOSPHORUS', 'POTASSIUM')
            
        Returns:
            Status string ('LOW', 'MEDIUM', 'HIGH')
        """
        thresholds = self.THRESHOLDS[nutrient]
        
        if value < thresholds['LOW']:
            return 'LOW'
        elif value < thresholds['MEDIUM']:
            return 'MEDIUM'
        elif value < thresholds['HIGH']:
            return 'MEDIUM'
        else:
            return 'HIGH'
    
    def _get_overall_status(self, avg_value, n, p, k):
        """
        Get overall fertility status
        
        Args:
            avg_value: Average of all NPK values
            n: Nitrogen value
            p: Phosphorus value
            k: Potassium value
            
        Returns:
            Overall status ('LOW', 'MEDIUM', 'HIGH')
        """
        # Count low nutrients
        low_count = sum([
            1 if self._get_status(n, 'NITROGEN') == 'LOW' else 0,
            1 if self._get_status(p, 'PHOSPHORUS') == 'LOW' else 0,
            1 if self._get_status(k, 'POTASSIUM') == 'LOW' else 0
        ])
        
        # If 2+ nutrients are low, overall is LOW
        if low_count >= 2:
            return 'LOW'
        elif low_count == 1:
            return 'MEDIUM'
        else:
            # Check if all are high
            high_count = sum([
                1 if self._get_status(n, 'NITROGEN') == 'HIGH' else 0,
                1 if self._get_status(p, 'PHOSPHORUS') == 'HIGH' else 0,
                1 if self._get_status(k, 'POTASSIUM') == 'HIGH' else 0
            ])
            
            if high_count >= 2:
                return 'HIGH'
            else:
                return 'MEDIUM'


"""
Recommendation Engine
Provides pest control and fertilizer recommendations
"""


class RecommendationEngine:
    """Generates recommendations based on pest detection and soil analysis"""
    
    # Pest-specific treatment recommendations
    PEST_TREATMENTS = {
        0: {  # Aphids
            'name': 'Aphids',
            'treatments': [
                'Neem Oil Spray: Mix 2-3ml neem oil per liter of water and spray on affected plants',
                'Insecticidal Soap: Apply soap solution (5ml per liter) to leaves',
                'Ladybugs: Introduce beneficial insects for biological control',
                'Pruning: Remove heavily infested leaves and branches'
            ],
            'prevention': [
                'Regular monitoring of plants',
                'Maintain plant health with proper watering',
                'Avoid excessive nitrogen fertilization'
            ]
        },
        1: {  # Locusts
            'name': 'Locusts',
            'treatments': [
                'Chemical Insecticides: Use approved insecticides like Malathion or Fenitrothion',
                'Biological Control: Introduce natural predators like birds',
                'Barrier Methods: Use fine mesh nets to protect crops',
                'Early Detection: Monitor and control nymph stages'
            ],
            'prevention': [
                'Early warning systems',
                'Community-level pest management',
                'Crop rotation and diversification'
            ]
        },
        2: {  # Beetles
            'name': 'Beetles',
            'treatments': [
                'Hand Picking: Remove beetles manually during early morning',
                'Neem Oil: Apply neem-based insecticides',
                'Diatomaceous Earth: Sprinkle around plant base',
                'Pyrethrin-based Sprays: Use natural pyrethrum insecticides'
            ],
            'prevention': [
                'Crop rotation',
                'Remove crop residues after harvest',
                'Use row covers during planting season'
            ]
        },
        3: {  # Caterpillars
            'name': 'Caterpillars',
            'treatments': [
                'Bacillus thuringiensis (Bt): Apply biological insecticide',
                'Neem Oil Spray: Effective against young caterpillars',
                'Hand Picking: Remove visible caterpillars',
                'Spinosad: Use organic insecticide for heavy infestations'
            ],
            'prevention': [
                'Regular scouting and monitoring',
                'Encourage natural predators',
                'Clean garden debris to remove pupae'
            ]
        }
    }
    
    # Fertilizer recommendations based on nutrient deficiencies
    FERTILIZER_RECOMMENDATIONS = {
        'LOW_NITROGEN': {
            'fertilizers': [
                'Urea (46-0-0): Apply 100-150 kg/hectare',
                'Ammonium Sulfate (21-0-0): Apply 200-250 kg/hectare',
                'Compost: Apply well-decomposed organic manure (5-10 tons/hectare)'
            ],
            'application': 'Apply nitrogen fertilizers in split doses during growing season'
        },
        'LOW_PHOSPHORUS': {
            'fertilizers': [
                'Single Super Phosphate (SSP): Apply 200-300 kg/hectare',
                'Diammonium Phosphate (DAP) (18-46-0): Apply 150-200 kg/hectare',
                'Rock Phosphate: Apply 500-1000 kg/hectare for long-term supply',
                'Bone Meal: Organic option, apply 500-1000 kg/hectare'
            ],
            'application': 'Apply phosphorus at planting time as it is less mobile in soil'
        },
        'LOW_POTASSIUM': {
            'fertilizers': [
                'Muriate of Potash (MOP) (0-0-60): Apply 100-150 kg/hectare',
                'Sulfate of Potash (0-0-50): Apply 120-180 kg/hectare',
                'Wood Ash: Organic source, apply 500-1000 kg/hectare',
                'Potassium Sulfate: For crops sensitive to chloride'
            ],
            'application': 'Apply potassium before or during early growth stages'
        }
    }
    
    def __init__(self):
        """Initialize recommendation engine"""
        pass
    
    def get_pest_recommendations(self, pest_class):
        """
        Get pest control recommendations
        
        Args:
            pest_class: Predicted pest class index
            
        Returns:
            Dictionary with pest treatment recommendations
        """
        if pest_class in self.PEST_TREATMENTS:
            return self.PEST_TREATMENTS[pest_class]
        else:
            return {
                'name': 'Unknown Pest',
                'treatments': ['Consult with agricultural extension officer'],
                'prevention': ['Regular monitoring and proper plant care']
            }
    
    def get_fertilizer_recommendations(self, imbalances):
        """
        Get fertilizer recommendations based on nutrient imbalances
        
        Args:
            imbalances: List of imbalance strings (e.g., ['LOW_NITROGEN', 'LOW_PHOSPHORUS'])
            
        Returns:
            Dictionary with fertilizer recommendations
        """
        recommendations = {
            'deficiencies': [],
            'fertilizers': [],
            'application_notes': []
        }
        
        for imbalance in imbalances:
            if imbalance in self.FERTILIZER_RECOMMENDATIONS:
                rec = self.FERTILIZER_RECOMMENDATIONS[imbalance]
                recommendations['deficiencies'].append(imbalance)
                recommendations['fertilizers'].extend(rec['fertilizers'])
                recommendations['application_notes'].append(rec['application'])
        
        # Remove duplicates
        recommendations['fertilizers'] = list(set(recommendations['fertilizers']))
        recommendations['application_notes'] = list(set(recommendations['application_notes']))
        
        return recommendations
    
    def get_combined_recommendations(self, pest_class, soil_analysis):
        """
        Get combined recommendations for pest and soil
        
        Args:
            pest_class: Predicted pest class index
            soil_analysis: Soil analysis results dictionary
            
        Returns:
            Dictionary with combined recommendations
        """
        pest_rec = self.get_pest_recommendations(pest_class)
        fertilizer_rec = self.get_fertilizer_recommendations(soil_analysis.get('imbalances', []))
        
        return {
            'pest_recommendations': pest_rec,
            'fertilizer_recommendations': fertilizer_rec,
            'summary': self._generate_summary(pest_rec, fertilizer_rec, soil_analysis)
        }
    
    def _generate_summary(self, pest_rec, fertilizer_rec, soil_analysis):
        """Generate summary of recommendations"""
        summary_points = []
        
        # Pest summary
        summary_points.append(f"Detected pest: {pest_rec['name']}")
        summary_points.append(f"Primary treatment: {pest_rec['treatments'][0]}")
        
        # Soil summary
        if soil_analysis.get('overall_status'):
            summary_points.append(f"Soil fertility: {soil_analysis['overall_status']}")
        
        if fertilizer_rec['deficiencies']:
            summary_points.append(f"Nutrient deficiencies detected: {', '.join(fertilizer_rec['deficiencies'])}")
            summary_points.append(f"Recommended fertilizer: {fertilizer_rec['fertilizers'][0] if fertilizer_rec['fertilizers'] else 'None'}")
        else:
            summary_points.append("Soil nutrient levels are adequate")
        
        return summary_points


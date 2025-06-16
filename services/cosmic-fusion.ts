// frontend/src/services/cosmic-fusion.ts

import { AstrologyService } from './astrology.js';
import { NumerologyService } from './numerology.js';
import { FeedbackService } from './feedback.js';

export interface CosmicProfile {
  fusedInsights: {
    cosmicAlignment: number; // 0-10 scale
    archetypeSummary: string;
    keyTraits: {
      destiny: number;
      soulUrge: number;
      personality: number;
    };
    energyVectors: {
      love: number;
      career: number;
      health: number;
      finance: number;
      spiritual: number;
      overall: number;
    };
  };
  sunSign: string;
  numerologyCore: {
    destiny: number;
    soulUrge: number;
    personality: number;
  };
  birthday: number;
}

export interface EnhancedDailyInsight {
  energyReadings: {
    overall: number;
    love: number;
    career: number;
    health: number;
    finance: number;
  };
  manifestationPower: number; // 0-10 scale
  spiritualFocus: string;
  optimalActivities: string[];
  cautionAreas: string[];
  cosmicInfluences: string[];
  personalizedGuidance: string[];
}

export class CosmicFusionService {

  // Fuse astrology + numerology + birthday into cosmic profile object
  static generateCosmicProfile(
    sunSign: string,
    destiny: number,
    soulUrge: number,
    personality: number,
    lifePath: number,
    birthday: number
  ): CosmicProfile {

    // 1. Calculate base numerology traits weighted average
    const keyTraits = {
      destiny,
      soulUrge,
      personality,
    };

    // 2. Astrological archetype influence (simplified: can extend with ephemeris data)
    const archetypeSummary = AstrologyService.getArchetypeSummary(sunSign);

    // 3. Energy vectors by combining numerology and astrology
    // Sample weights for traits (scale 1-10)
    const loveEnergy = (destiny * 0.4 + personality * 0.4 + AstrologyService.getLoveInfluence(sunSign) * 0.2);
    const careerEnergy = (destiny * 0.5 + soulUrge * 0.3 + AstrologyService.getCareerInfluence(sunSign) * 0.2);
    const healthEnergy = (personality * 0.5 + AstrologyService.getHealthInfluence(sunSign) * 0.5);
    const financeEnergy = (destiny * 0.6 + soulUrge * 0.2 + AstrologyService.getFinanceInfluence(sunSign) * 0.2);
    const spiritualEnergy = (soulUrge * 0.5 + AstrologyService.getSpiritualInfluence(sunSign) * 0.5);

    // Normalize to 0-10 scale
    const normalize = (val: number) => Math.min(10, Math.max(0, val));

    const energyVectors = {
      love: normalize(loveEnergy),
      career: normalize(careerEnergy),
      health: normalize(healthEnergy),
      finance: normalize(financeEnergy),
      spiritual: normalize(spiritualEnergy),
      overall: 0 // to compute next
    };
    energyVectors.overall = normalize(
      (energyVectors.love + energyVectors.career + energyVectors.health + energyVectors.finance + energyVectors.spiritual) / 5
    );

    // 4. Compute cosmic alignment score by blending energy overall and birthday numerology (e.g., birth day mod 10)
    // Example: birthday mod 10 scaled to 0-10, averaged with overall energy
    const birthdayFactor = (birthday % 10);
    const cosmicAlignment = normalize((energyVectors.overall + birthdayFactor) / 2);

    return {
      fusedInsights: {
        cosmicAlignment,
        archetypeSummary,
        keyTraits,
        energyVectors,
      },
      sunSign,
      numerologyCore: { destiny, soulUrge, personality },
      birthday,
    };
  }

  // Generate enhanced daily insight using cosmic profile + date + AI feedback
  static generateEnhancedDailyInsight(
    cosmicProfile: CosmicProfile,
    targetDate: string,
    learningInsights: any // object returned from FeedbackService with accuracy, sample counts etc
  ): EnhancedDailyInsight {

    // 1. Extract base energy vectors
    const baseEnergies = cosmicProfile.fusedInsights.energyVectors;

    // 2. Calculate modifiers from astrological transits (mock example)
    // Real implementation should query AstrologyService with targetDate for transits/aspects
    const transitModifiers = this.getTransitModifiers(cosmicProfile.sunSign, targetDate);

    // 3. Calculate numerology cycle modifiers for targetDate (e.g., personal year cycle)
    const numerologyModifiers = this.getNumerologyCycleModifiers(cosmicProfile.numerologyCore.destiny, targetDate);

    // 4. Combine base energy with modifiers weighted by AI feedback confidence
    const confidenceWeight = learningInsights?.accuracy_metrics?.overall
      ? Math.min(1, learningInsights.accuracy_metrics.overall / 10)
      : 0.7; // default confidence

    const combinedEnergy = (base: number, transitMod: number, numMod: number) => {
      return Math.min(
        10,
        Math.max(
          0,
          base * (1 - confidenceWeight) +
          ((transitMod + numMod) / 2) * confidenceWeight
        )
      );
    };

    const overall = combinedEnergy(baseEnergies.overall, transitModifiers.overall, numerologyModifiers.overall);
    const love = combinedEnergy(baseEnergies.love, transitModifiers.love, numerologyModifiers.love);
    const career = combinedEnergy(baseEnergies.career, transitModifiers.career, numerologyModifiers.career);
    const health = combinedEnergy(baseEnergies.health, transitModifiers.health, numerologyModifiers.health);
    const finance = combinedEnergy(baseEnergies.finance, transitModifiers.finance, numerologyModifiers.finance);

    // 5. Manifestation power derived from overall and spiritual energies, weighted by feedback
    const manifestationPower = Math.round(
      (overall * 0.6 + baseEnergies.spiritual * 0.4) * confidenceWeight
    );

    // 6. Spiritual focus - generate dynamic message based on spiritual energy
    const spiritualFocus = this.getSpiritualFocusMessage(baseEnergies.spiritual);

    // 7. Recommended activities and caution areas based on thresholds
    const optimalActivities = this.getOptimalActivities({ overall, love, career, health, finance });
    const cautionAreas = this.getCautionAreas({ overall, love, career, health, finance });

    // 8. Cosmic influences and personalized guidance placeholders (expand with NLP/AI in future)
    const cosmicInfluences = [
      `Your sun sign ${cosmicProfile.sunSign} supports new beginnings today.`,
      `Numerology destiny number ${cosmicProfile.numerologyCore.destiny} encourages persistence and focus.`
    ];

    const personalizedGuidance = [
      'Stay open to unexpected opportunities.',
      'Practice mindfulness to enhance clarity.'
    ];

    return {
      energyReadings: { overall, love, career, health, finance },
      manifestationPower,
      spiritualFocus,
      optimalActivities,
      cautionAreas,
      cosmicInfluences,
      personalizedGuidance,
    };
  }

  // Helpers:

  private static getTransitModifiers(sunSign: string, targetDate: string) {
    // Placeholder for actual astrology transit computations
    // Return modifiers in 0-10 scale for energy categories
    // Simulate mild daily variation
    return {
      overall: 5 + Math.sin(new Date(targetDate).getDate()) * 2,
      love: 5 + Math.cos(new Date(targetDate).getDate()) * 2,
      career: 5 + Math.sin(new Date(targetDate).getDate() / 2) * 2,
      health: 5 + Math.cos(new Date(targetDate).getDate() / 3) * 2,
      finance: 5 + Math.sin(new Date(targetDate).getDate() / 4) * 2,
    };
  }

  private static getNumerologyCycleModifiers(destinyNumber: number, targetDate: string) {
    // Placeholder: calculate numerology personal year or pinnacle cycles
    // For now, cycle modulates energies by +/- 1 based on day parity
    const day = new Date(targetDate).getDate();
    const mod = (day % 2 === 0) ? 1 : -1;
    const base = 5;

    return {
      overall: base + mod,
      love: base + mod * 0.8,
      career: base + mod * 0.9,
      health: base + mod * 0.7,
      finance: base + mod * 0.85,
    };
  }

  private static getSpiritualFocusMessage(spiritualEnergy: number): string {
    if (spiritualEnergy >= 8) return 'High spiritual awareness; ideal for meditation and inner work.';
    if (spiritualEnergy >= 5) return 'Balanced spiritual energy; practice gratitude.';
    if (spiritualEnergy >= 3) return 'Low spiritual energy; focus on grounding activities.';
    return 'Minimal spiritual energy today; prioritize rest and recuperation.';
  }

  private static getOptimalActivities(energies: Record<string, number>): string[] {
    const activities: string[] = [];
    if (energies.overall >= 7) activities.push('Initiate new projects');
    if (energies.love >= 7) activities.push('Romantic engagements', 'Social bonding');
    if (energies.career >= 7) activities.push('Career advancement tasks', 'Networking');
    if (energies.health >= 7) activities.push('Physical exercise', 'Wellness activities');
    if (energies.finance >= 7) activities.push('Financial planning', 'Investments');
    if (activities.length === 0) activities.push('Rest and reflection');
    return activities;
  }

  private static getCautionAreas(energies: Record<string, number>): string[] {
    const cautions: string[] = [];
    if (energies.overall <= 3) cautions.push('Avoid big decisions', 'Rest more');
    if (energies.love <= 3) cautions.push('Avoid relationship conflicts');
    if (energies.career <= 3) cautions.push('Delay negotiations');
    if (energies.health <= 3) cautions.push('Prioritize recovery');
    if (energies.finance <= 3) cautions.push('Avoid risky financial moves');
    if (cautions.length === 0) cautions.push('Maintain balance and focus');
    return cautions;
  }
}
